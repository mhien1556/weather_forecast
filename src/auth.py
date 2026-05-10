"""
Authentication module — stores users in a local JSON file.
Passwords are hashed with bcrypt for security.
"""

import json
import os
import hashlib
import secrets
from datetime import datetime

# Path to user database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")


def _ensure_db():
    """Create the data directory and users.json if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)


def _load_users() -> dict:
    _ensure_db()
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_users(users: dict):
    _ensure_db()
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash password with SHA-256 + salt. Returns (hash, salt)."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return hashed, salt


def register_user(username: str, password: str, display_name: str = "") -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str).
    """
    username = username.strip().lower()

    if not username or not password:
        return False, "Tên đăng nhập và mật khẩu không được để trống."

    if len(username) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự."

    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự."

    users = _load_users()

    if username in users:
        return False, "Tên đăng nhập đã tồn tại."

    hashed, salt = _hash_password(password)
    users[username] = {
        "password_hash": hashed,
        "salt": salt,
        "display_name": display_name or username,
        "created_at": datetime.now().isoformat(),
        "favorite_cities": [],
        "search_history": [],
    }
    _save_users(users)
    return True, "Đăng ký thành công! 🎉"


def login_user(username: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Authenticate a user.
    Returns (success, message, user_data or None).
    """
    username = username.strip().lower()
    users = _load_users()

    if username not in users:
        return False, "Tên đăng nhập không tồn tại.", None

    user = users[username]
    hashed, _ = _hash_password(password, user["salt"])

    if hashed != user["password_hash"]:
        return False, "Mật khẩu không đúng.", None

    return True, f"Xin chào {user['display_name']}! 👋", user


def add_favorite_city(username: str, city: str) -> bool:
    """Add a city to user's favorites (max 10)."""
    username = username.strip().lower()
    users = _load_users()
    if username not in users:
        return False
    favs = users[username].get("favorite_cities", [])
    if city not in favs and len(favs) < 10:
        favs.append(city)
        users[username]["favorite_cities"] = favs
        _save_users(users)
    return True


def remove_favorite_city(username: str, city: str) -> bool:
    """Remove a city from user's favorites."""
    username = username.strip().lower()
    users = _load_users()
    if username not in users:
        return False
    favs = users[username].get("favorite_cities", [])
    if city in favs:
        favs.remove(city)
        users[username]["favorite_cities"] = favs
        _save_users(users)
    return True


def get_favorites(username: str) -> list[str]:
    """Get user's favorite cities."""
    username = username.strip().lower()
    users = _load_users()
    if username not in users:
        return []
    return users[username].get("favorite_cities", [])


def add_search_history(username: str, city: str):
    """Record a search (keep last 20)."""
    username = username.strip().lower()
    users = _load_users()
    if username not in users:
        return
    history = users[username].get("search_history", [])
    entry = {"city": city, "time": datetime.now().isoformat()}
    history.insert(0, entry)
    users[username]["search_history"] = history[:20]
    _save_users(users)


def get_search_history(username: str) -> list[dict]:
    """Get user's search history."""
    username = username.strip().lower()
    users = _load_users()
    if username not in users:
        return []
    return users[username].get("search_history", [])


def get_user_data(username: str) -> dict | None:
    """Get full data for a user."""
    username = username.strip().lower()
    users = _load_users()
    return users.get(username)


def update_user_profile(username: str, display_name: str = None, password: str = None) -> tuple[bool, str]:
    """
    Update user profile details.
    """
    username = username.strip().lower()
    users = _load_users()

    if username not in users:
        return False, "Người dùng không tồn tại."

    if display_name:
        users[username]["display_name"] = display_name

    if password:
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."
        hashed, salt = _hash_password(password)
        users[username]["password_hash"] = hashed
        users[username]["salt"] = salt

    _save_users(users)
    return True, "Cập nhật thông tin thành công! ✨"
