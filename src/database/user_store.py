"""Quản lý user: sử dụng SQLite với schema chuẩn hóa (5 bảng)."""
import sqlite3
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(os.path.dirname(__file__)) / '..' / '..' / 'data' / 'users.db'

SECURITY_QUESTIONS = [
    'Tên thú cưng đầu tiên của bạn?',
    'Tên trường tiểu học bạn đã học?',
    'Tên thành phố bạn sinh ra?',
    'Món ăn yêu thích của bạn?',
    'Tên người thầy/cô giáo bạn nhớ nhất?',
]

def get_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ── Khởi tạo DB ──────────────────────────────────────────────────────────────

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ── Bảng 1: users ──
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT,
            role TEXT DEFAULT 'user',
            avatar TEXT,
            security_question TEXT,
            security_answer TEXT,
            created_at TEXT,
            updated_at TEXT,
            favorites TEXT,
            history TEXT
        )
    ''')

    # ── Bảng 2: user_settings ──
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            theme TEXT DEFAULT 'dark',
            unit_temp TEXT DEFAULT 'C',
            unit_wind TEXT DEFAULT 'km/h',
            unit_pressure TEXT DEFAULT 'hPa',
            unit_visibility TEXT DEFAULT 'km',
            dynamic_bg INTEGER DEFAULT 1,
            language TEXT DEFAULT 'vi',
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')

    # ── Bảng 3: search_history ──
    c.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            city TEXT NOT NULL,
            weather_brief TEXT DEFAULT '',
            searched_at TEXT,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')

    # ── Bảng 4: favorite_cities ──
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorite_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            city TEXT NOT NULL,
            added_at TEXT,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
            UNIQUE(username, city)
        )
    ''')

    # ── Migration dữ liệu cũ từ JSON sang bảng mới ──
    _migrate_old_data(c)

    # ── Khởi tạo admin mặc định ──
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    if count == 0:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''
            INSERT INTO users (username, name, email, password, role, avatar, 
                               security_question, security_answer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'admin', 'Quản trị viên', 'admin@example.com', _hash('admin'),
            'super_admin', 'A', '', '', now, now
        ))
        c.execute('''
            INSERT OR IGNORE INTO user_settings (username) VALUES (?)
        ''', ('admin',))

    conn.commit()
    conn.close()

def _migrate_old_data(cursor):
    """Migrate dữ liệu từ JSON columns sang bảng mới."""
    try:
        cursor.execute("SELECT username, favorites, history FROM users")
    except sqlite3.OperationalError:
        return

    rows = cursor.fetchall()
    for row in rows:
        username = row['username']
        
        # Migrate favorites
        try:
            favs = json.loads(row['favorites'] or '[]')
            if isinstance(favs, list):
                for city in favs:
                    if city:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        cursor.execute('''
                            INSERT OR IGNORE INTO favorite_cities (username, city, added_at)
                            VALUES (?, ?, ?)
                        ''', (username, city, now))
        except (json.JSONDecodeError, TypeError):
            pass

        # Migrate history
        try:
            hist = json.loads(row['history'] or '[]')
            if isinstance(hist, list):
                cursor.execute("SELECT COUNT(*) FROM search_history WHERE username = ?", (username,))
                if cursor.fetchone()[0] == 0:
                    for entry in hist:
                        if isinstance(entry, dict):
                            cursor.execute('''
                                INSERT INTO search_history (username, city, weather_brief, searched_at)
                                VALUES (?, ?, ?, ?)
                            ''', (username, entry.get('city', ''), entry.get('brief', ''), entry.get('time', '')))
        except (json.JSONDecodeError, TypeError):
            pass

        # Tạo user_settings mặc định
        cursor.execute('''
            INSERT OR IGNORE INTO user_settings (username) VALUES (?)
        ''', (username,))

        # Cập nhật timestamp nếu chưa có
        cursor.execute("SELECT created_at FROM users WHERE username = ?", (username,))
        r = cursor.fetchone()
        if r and not r['created_at']:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE users SET created_at = ?, updated_at = ? WHERE username = ?",
                           (now, now, username))

# ── Hàm tiện ích ──────────────────────────────────────────────────────────────

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _row_to_dict(row) -> dict:
    if not row:
        return None
    return dict(row)

# ── CRUD Users ────────────────────────────────────────────────────────────────

def get_all_users() -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, name, email, password, role, avatar, security_question, security_answer, created_at, updated_at FROM users")
    rows = c.fetchall()
    result = {}
    for r in rows:
        d = dict(r)
        d['favorites'] = get_favorites(d['username'])
        d['history'] = get_history(d['username'])
        result[d['username']] = d
    conn.close()
    return result

def save_user(user_dict: dict) -> None:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute("SELECT username FROM users WHERE username = ?", (user_dict['username'],))
    exists = c.fetchone()
    
    if exists:
        c.execute('''
            UPDATE users SET name=?, email=?, password=?, role=?, avatar=?,
                             security_question=?, security_answer=?, updated_at=?
            WHERE username=?
        ''', (
            user_dict.get('name', ''),
            user_dict.get('email', ''),
            user_dict.get('password', ''),
            user_dict.get('role', 'user'),
            user_dict.get('avatar', ''),
            user_dict.get('security_question', ''),
            user_dict.get('security_answer', ''),
            now,
            user_dict['username'],
        ))
    else:
        c.execute('''
            INSERT INTO users (username, name, email, password, role, avatar,
                               security_question, security_answer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_dict['username'],
            user_dict.get('name', ''),
            user_dict.get('email', ''),
            user_dict.get('password', ''),
            user_dict.get('role', 'user'),
            user_dict.get('avatar', ''),
            user_dict.get('security_question', ''),
            user_dict.get('security_answer', ''),
            now, now,
        ))

    c.execute("INSERT OR IGNORE INTO user_settings (username) VALUES (?)", (user_dict['username'],))

    if 'favorites' in user_dict and isinstance(user_dict['favorites'], list):
        for city in user_dict['favorites']:
            if city:
                c.execute('''
                    INSERT OR IGNORE INTO favorite_cities (username, city, added_at)
                    VALUES (?, ?, ?)
                ''', (user_dict['username'], city, now))

    conn.commit()
    conn.close()

def delete_user(username: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_user(username: str) -> dict | None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT username, name, email, password, role, avatar, 
                        security_question, security_answer, created_at, updated_at 
                 FROM users WHERE username = ?""", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d['favorites'] = get_favorites(username)
    d['history'] = get_history(username)
    return d

# ── Auth ──────────────────────────────────────────────────────────────────────

def login(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user and user['password'] == _hash(password):
        return user
    return None

def register(username: str, display_name: str, email: str, password: str,
             security_question: str = '', security_answer: str = '') -> dict | None:
    if get_user(username):
        return None
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        INSERT INTO users (username, name, email, password, role, avatar,
                           security_question, security_answer, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        username,
        display_name or username,
        email,
        _hash(password),
        'user',
        (display_name or username)[0].upper(),
        security_question,
        _hash(security_answer.strip().lower()) if security_answer else '',
        now, now,
    ))

    c.execute("INSERT INTO user_settings (username) VALUES (?)", (username,))

    conn.commit()
    conn.close()
    return get_user(username)

# ── Profile ───────────────────────────────────────────────────────────────────

def update_profile(username: str, name: str, email: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    if not c.fetchone():
        conn.close()
        return False
    avatar = name.strip()[0].upper() if name and name.strip() else '?'
    c.execute("""UPDATE users SET name=?, email=?, avatar=?, updated_at=? WHERE username=?""",
              (name.strip(), email.strip(), avatar, now, username))
    conn.commit()
    conn.close()
    return True

def change_password(username: str, old_pass: str, new_pass: str) -> bool:
    user = get_user(username)
    if not user or user['password'] != _hash(old_pass):
        return False
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE users SET password=?, updated_at=? WHERE username=?",
              (_hash(new_pass), now, username))
    conn.commit()
    conn.close()
    return True

def verify_security(username: str, answer: str) -> bool:
    user = get_user(username)
    if not user or not user.get('security_answer'):
        return False
    return user['security_answer'] == _hash(answer.strip().lower())

def reset_password(username: str, new_password: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    if not c.fetchone():
        conn.close()
        return False
    c.execute("UPDATE users SET password=?, updated_at=? WHERE username=?",
              (_hash(new_password), now, username))
    conn.commit()
    conn.close()
    return True

def get_security_question(username: str) -> str | None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT security_question FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row['security_question']:
        return row['security_question']
    return None

# ── Search History ───────────────────────────────────────────────────────────

def add_history(username: str, city: str, weather_brief: str = '') -> None:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%d/%m/%Y %H:%M')

    c.execute("DELETE FROM search_history WHERE username = ? AND LOWER(city) = LOWER(?)",
              (username, city))

    c.execute('''
        INSERT INTO search_history (username, city, weather_brief, searched_at)
        VALUES (?, ?, ?, ?)
    ''', (username, city, weather_brief, now))

    c.execute('''
        DELETE FROM search_history WHERE id NOT IN (
            SELECT id FROM search_history WHERE username = ?
            ORDER BY id DESC LIMIT 20
        ) AND username = ?
    ''', (username, username))

    conn.commit()
    conn.close()

def get_history(username: str) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT city, weather_brief AS brief, searched_at AS time
                 FROM search_history WHERE username = ?
                 ORDER BY id DESC LIMIT 20""", (username,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def clear_history(username: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM search_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# ── Favorites ────────────────────────────────────────────────────────────────

def get_favorites(username: str) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT city FROM favorite_cities WHERE username = ? ORDER BY id", (username,))
    rows = c.fetchall()
    conn.close()
    return [r['city'] for r in rows]

def add_favorite(username: str, city: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        c.execute('''
            INSERT OR IGNORE INTO favorite_cities (username, city, added_at)
            VALUES (?, ?, ?)
        ''', (username, city, now))
        conn.commit()
        inserted = c.rowcount > 0
    except Exception:
        inserted = False
    conn.close()
    return inserted

def remove_favorite(username: str, city: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM favorite_cities WHERE username = ? AND city = ?", (username, city))
    conn.commit()
    conn.close()

# ── User Settings ────────────────────────────────────────────────────────────

def get_user_settings(username: str) -> dict:
    defaults = {
        'theme': 'dark',
        'unit_temp': 'C',
        'unit_wind': 'km/h',
        'unit_pressure': 'hPa',
        'unit_visibility': 'km',
        'dynamic_bg': True,
        'language': 'vi',
    }
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT theme, unit_temp, unit_wind, unit_pressure, unit_visibility, dynamic_bg, language
                 FROM user_settings WHERE username = ?""", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return defaults
    return {
        'theme': row['theme'] or 'dark',
        'unit_temp': row['unit_temp'] or 'C',
        'unit_wind': row['unit_wind'] or 'km/h',
        'unit_pressure': row['unit_pressure'] or 'hPa',
        'unit_visibility': row['unit_visibility'] or 'km',
        'dynamic_bg': bool(row['dynamic_bg']),
        'language': row['language'] or 'vi',
    }

def update_user_settings(username: str, settings: dict) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_settings (username, theme, unit_temp, unit_wind, unit_pressure, unit_visibility, dynamic_bg, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            theme = excluded.theme,
            unit_temp = excluded.unit_temp,
            unit_wind = excluded.unit_wind,
            unit_pressure = excluded.unit_pressure,
            unit_visibility = excluded.unit_visibility,
            dynamic_bg = excluded.dynamic_bg,
            language = excluded.language
    ''', (
        username,
        settings.get('theme', 'dark'),
        settings.get('unit_temp', 'C'),
        settings.get('unit_wind', 'km/h'),
        settings.get('unit_pressure', 'hPa'),
        settings.get('unit_visibility', 'km'),
        1 if settings.get('dynamic_bg', True) else 0,
        settings.get('language', 'vi'),
    ))
    conn.commit()
    conn.close()

# Khởi tạo db khi module được import
init_db()