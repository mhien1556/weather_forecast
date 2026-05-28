"""Quản lý user: lưu vào JSON, hash password, câu hỏi bảo mật, lịch sử, yêu thích."""
import hashlib
import json
import os
from datetime import datetime

_USERS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')

SECURITY_QUESTIONS = [
    'Tên thú cưng đầu tiên của bạn?',
    'Tên trường tiểu học bạn đã học?',
    'Tên thành phố bạn sinh ra?',
    'Món ăn yêu thích của bạn?',
    'Tên người thầy/cô giáo bạn nhớ nhất?',
]


def _load() -> dict:
    os.makedirs(os.path.dirname(_USERS_FILE), exist_ok=True)
    if not os.path.exists(_USERS_FILE):
        _save({})
    with open(_USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(users: dict) -> None:
    with open(_USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login(username: str, password: str) -> dict | None:
    users = _load()
    user = users.get(username)
    if user and user['password'] == _hash(password):
        return user
    return None


def register(username: str, display_name: str, email: str, password: str,
             security_question: str = '', security_answer: str = '') -> dict | None:
    users = _load()
    if username in users:
        return None
    user = {
        'username': username,
        'name': display_name or username,
        'email': email,
        'password': _hash(password),
        'avatar': (display_name or username)[0].upper(),
        'security_question': security_question,
        'security_answer': _hash(security_answer.strip().lower()) if security_answer else '',
        'favorites': [],
        'history': [],
        'notifications': {'rain': True, 'extreme': True, 'daily': False},
    }
    users[username] = user
    _save(users)
    return user


def get_user(username: str) -> dict | None:
    return _load().get(username)


def update_profile(username: str, name: str, email: str) -> bool:
    users = _load()
    if username not in users:
        return False
    users[username]['name'] = name.strip()
    users[username]['email'] = email.strip()
    users[username]['avatar'] = name.strip()[0].upper() if name.strip() else '?'
    _save(users)
    return True


def change_password(username: str, old_pass: str, new_pass: str) -> bool:
    users = _load()
    user = users.get(username)
    if not user or user['password'] != _hash(old_pass):
        return False
    users[username]['password'] = _hash(new_pass)
    _save(users)
    return True


def verify_security(username: str, answer: str) -> bool:
    users = _load()
    user = users.get(username)
    if not user or not user.get('security_answer'):
        return False
    return user['security_answer'] == _hash(answer.strip().lower())


def reset_password(username: str, new_password: str) -> bool:
    users = _load()
    if username not in users:
        return False
    users[username]['password'] = _hash(new_password)
    _save(users)
    return True


def get_security_question(username: str) -> str | None:
    users = _load()
    user = users.get(username)
    if user and user.get('security_question'):
        return user['security_question']
    return None


# ── Lịch sử truy cập ─────────────────────────────────────────
def add_history(username: str, city: str, weather_brief: str = '') -> None:
    users = _load()
    if username not in users:
        return
    history = users[username].setdefault('history', [])
    entry = {
        'city': city,
        'brief': weather_brief,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }
    # Xóa trùng
    history = [h for h in history if h['city'].lower() != city.lower()]
    history.insert(0, entry)
    users[username]['history'] = history[:20]  # giữ tối đa 20
    _save(users)


def get_history(username: str) -> list:
    users = _load()
    if username in users and 'history' not in users[username]:
        users[username]['history'] = []
        _save(users)
    return users.get(username, {}).get('history', [])


def clear_history(username: str) -> None:
    users = _load()
    if username in users:
        users[username]['history'] = []
        _save(users)


# ── Thành phố yêu thích ───────────────────────────────────────
def get_favorites(username: str) -> list:
    users = _load()
    if username in users and 'favorites' not in users[username]:
        users[username]['favorites'] = []
        _save(users)
    return users.get(username, {}).get('favorites', [])


def add_favorite(username: str, city: str) -> bool:
    users = _load()
    if username not in users:
        return False
    favs = users[username].setdefault('favorites', [])
    if city not in favs:
        favs.append(city)
        _save(users)
        return True
    return False


def remove_favorite(username: str, city: str) -> None:
    users = _load()
    if username in users:
        users[username]['favorites'] = [f for f in users[username].get('favorites', []) if f != city]
        _save(users)


# ── Cài đặt thông báo ─────────────────────────────────────────
def get_notifications(username: str) -> dict:
    users = _load()
    default = {'rain': True, 'extreme': True, 'daily': False}
    if username in users and 'notifications' not in users[username]:
        users[username]['notifications'] = default
        _save(users)
    return users.get(username, {}).get('notifications', default)


def update_notifications(username: str, settings: dict) -> None:
    users = _load()
    if username in users:
        users[username]['notifications'] = settings
        _save(users)
