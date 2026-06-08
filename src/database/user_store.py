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

    # ── Bảng 1: users (thông tin chính) ──
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
            -- Giữ lại cột cũ để tương thích migration
            favorites TEXT,
            history TEXT,
            notifications TEXT
        )
    ''')

    # ── Bảng 2: user_settings (cài đặt giao diện & đơn vị) ──
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
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')

    # ── Bảng 3: search_history (lịch sử tìm kiếm) ──
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

    # ── Bảng 4: favorite_cities (thành phố yêu thích) ──
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

    # ── Bảng 5: notification_settings (cài đặt thông báo) ──
    c.execute('''
        CREATE TABLE IF NOT EXISTS notification_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            rain_alert INTEGER DEFAULT 1,
            extreme_alert INTEGER DEFAULT 1,
            daily_report INTEGER DEFAULT 0,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')

    # ── Thêm cột created_at, updated_at nếu bảng users cũ chưa có ──
    try:
        c.execute("SELECT created_at FROM users LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
        c.execute("ALTER TABLE users ADD COLUMN updated_at TEXT")

    # ── Migration: chuyển dữ liệu JSON cũ sang bảng mới ──
    _migrate_old_data(c)

    # ── Khởi tạo tài khoản admin mặc định nếu chưa có ──
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
            INSERT OR IGNORE INTO notification_settings (username, rain_alert, extreme_alert, daily_report)
            VALUES (?, 1, 1, 0)
        ''', ('admin',))
        c.execute('''
            INSERT OR IGNORE INTO user_settings (username) VALUES (?)
        ''', ('admin',))

    conn.commit()
    conn.close()


def _migrate_old_data(cursor):
    """Migrate dữ liệu từ JSON columns (favorites, history, notifications) sang bảng mới."""
    try:
        cursor.execute("SELECT username, favorites, history, notifications FROM users")
    except sqlite3.OperationalError:
        return  # Bảng users chưa có cột cũ → không cần migrate

    rows = cursor.fetchall()
    for row in rows:
        username = row['username']
        
        # ── Migrate favorites ──
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

        # ── Migrate history ──
        try:
            hist = json.loads(row['history'] or '[]')
            if isinstance(hist, list):
                # Kiểm tra xem đã migrate chưa
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

        # ── Migrate notifications ──
        try:
            notifs = json.loads(row['notifications'] or '{}')
            if isinstance(notifs, dict):
                cursor.execute('''
                    INSERT OR IGNORE INTO notification_settings (username, rain_alert, extreme_alert, daily_report)
                    VALUES (?, ?, ?, ?)
                ''', (
                    username,
                    1 if notifs.get('rain', True) else 0,
                    1 if notifs.get('extreme', True) else 0,
                    1 if notifs.get('daily', False) else 0,
                ))
        except (json.JSONDecodeError, TypeError):
            pass

        # ── Tạo user_settings mặc định nếu chưa có ──
        cursor.execute('''
            INSERT OR IGNORE INTO user_settings (username) VALUES (?)
        ''', (username,))

        # ── Cập nhật timestamp nếu chưa có ──
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
        # Đính kèm favorites, history, notifications từ bảng mới
        d['favorites'] = get_favorites(d['username'])
        d['history'] = get_history(d['username'])
        d['notifications'] = get_notifications(d['username'])
        result[d['username']] = d
    conn.close()
    return result


def save_user(user_dict: dict) -> None:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Kiểm tra user đã tồn tại chưa
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

    # Đảm bảo có bản ghi ở bảng liên quan
    c.execute("INSERT OR IGNORE INTO user_settings (username) VALUES (?)", (user_dict['username'],))
    c.execute('''
        INSERT OR IGNORE INTO notification_settings (username, rain_alert, extreme_alert, daily_report)
        VALUES (?, ?, ?, ?)
    ''', (
        user_dict['username'],
        1 if user_dict.get('notifications', {}).get('rain', True) else 0,
        1 if user_dict.get('notifications', {}).get('extreme', True) else 0,
        1 if user_dict.get('notifications', {}).get('daily', False) else 0,
    ))

    # Nếu có favorites trong dict, đồng bộ sang bảng mới
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
    # CASCADE sẽ tự xóa dữ liệu liên quan
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
    d['notifications'] = get_notifications(username)
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
    c.execute('''
        INSERT INTO notification_settings (username, rain_alert, extreme_alert, daily_report)
        VALUES (?, 1, 1, 0)
    ''', (username,))

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


# ── Search History (bảng search_history) ──────────────────────────────────────

def add_history(username: str, city: str, weather_brief: str = '') -> None:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%d/%m/%Y %H:%M')

    # Xóa bản ghi cũ cùng thành phố (giữ mới nhất)
    c.execute("DELETE FROM search_history WHERE username = ? AND LOWER(city) = LOWER(?)",
              (username, city))

    c.execute('''
        INSERT INTO search_history (username, city, weather_brief, searched_at)
        VALUES (?, ?, ?, ?)
    ''', (username, city, weather_brief, now))

    # Giữ tối đa 20 bản ghi
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


# ── Favorites (bảng favorite_cities) ──────────────────────────────────────────

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


# ── Notifications (bảng notification_settings) ───────────────────────────────

def get_notifications(username: str) -> dict:
    default = {'rain': True, 'extreme': True, 'daily': False}
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT rain_alert, extreme_alert, daily_report FROM notification_settings WHERE username = ?",
              (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return default
    return {
        'rain': bool(row['rain_alert']),
        'extreme': bool(row['extreme_alert']),
        'daily': bool(row['daily_report']),
    }


def update_notifications(username: str, settings: dict) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO notification_settings (username, rain_alert, extreme_alert, daily_report)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            rain_alert = excluded.rain_alert,
            extreme_alert = excluded.extreme_alert,
            daily_report = excluded.daily_report
    ''', (
        username,
        1 if settings.get('rain', True) else 0,
        1 if settings.get('extreme', True) else 0,
        1 if settings.get('daily', False) else 0,
    ))
    conn.commit()
    conn.close()


# ── User Settings (bảng user_settings) ───────────────────────────────────────

def get_user_settings(username: str) -> dict:
    """Trả về cài đặt giao diện & đơn vị từ DB."""
    defaults = {
        'theme': 'dark',
        'unit_temp': 'C',
        'unit_wind': 'km/h',
        'unit_pressure': 'hPa',
        'unit_visibility': 'km',
        'dynamic_bg': True,
    }
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT theme, unit_temp, unit_wind, unit_pressure, unit_visibility, dynamic_bg
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
    }


def update_user_settings(username: str, settings: dict) -> None:
    """Cập nhật cài đặt giao diện & đơn vị vào DB."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_settings (username, theme, unit_temp, unit_wind, unit_pressure, unit_visibility, dynamic_bg)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            theme = excluded.theme,
            unit_temp = excluded.unit_temp,
            unit_wind = excluded.unit_wind,
            unit_pressure = excluded.unit_pressure,
            unit_visibility = excluded.unit_visibility,
            dynamic_bg = excluded.dynamic_bg
    ''', (
        username,
        settings.get('theme', 'dark'),
        settings.get('unit_temp', 'C'),
        settings.get('unit_wind', 'km/h'),
        settings.get('unit_pressure', 'hPa'),
        settings.get('unit_visibility', 'km'),
        1 if settings.get('dynamic_bg', True) else 0,
    ))
    conn.commit()
    conn.close()


# Khởi tạo db khi module được import
init_db()
