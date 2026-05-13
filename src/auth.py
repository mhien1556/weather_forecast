"""
Authentication — stores users in a local JSON file.
Passwords are hashed with SHA-256 + random salt.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
from datetime import datetime

_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "users.json",
)


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────

def _ensure_db() -> None:
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    if not os.path.exists(_DB_PATH):
        with open(_DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)


def _load() -> dict:
    _ensure_db()
    with open(_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(users: dict) -> None:
    _ensure_db()
    with open(_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def _hash(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode()).hexdigest()
    return digest, salt


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def register_user(username: str, password: str, display_name: str = "") -> tuple[bool, str]:
    username = username.strip().lower()

    if len(username) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự."
    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự."

    users = _load()
    if username in users:
        return False, "Tên đăng nhập đã tồn tại."

    hashed, salt = _hash(password)
    users[username] = {
        "password_hash":  hashed,
        "salt":           salt,
        "display_name":   display_name.strip() or username,
        "avatar":         "🙂",
        "created_at":     datetime.now().isoformat(),
        "favorite_cities": [],
        "search_history":  [],
    }
    _save(users)
    return True, "Đăng ký thành công! 🎉"


def login_user(username: str, password: str) -> tuple[bool, str, dict | None]:
    username = username.strip().lower()
    users    = _load()

    if username not in users:
        return False, "Tên đăng nhập không tồn tại.", None

    user = users[username]
    digest, _ = _hash(password, user["salt"])
    if digest != user["password_hash"]:
        return False, "Mật khẩu không đúng.", None

    return True, f"Xin chào {user['display_name']}! 👋", user


def get_user_data(username: str) -> dict | None:
    return _load().get(username.strip().lower())


def update_user_profile(
    username: str,
    display_name: str | None = None,
    password: str | None = None,
    avatar: str | None = None,
) -> tuple[bool, str]:
    username = username.strip().lower()
    users    = _load()

    if username not in users:
        return False, "Người dùng không tồn tại."

    if display_name:
        users[username]["display_name"] = display_name.strip()

    if avatar:
        users[username]["avatar"] = avatar

    if password:
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."
        hashed, salt = _hash(password)
        users[username]["password_hash"] = hashed
        users[username]["salt"]          = salt

    _save(users)
    return True, "Cập nhật thành công! ✨"


def add_favorite_city(username: str, city: str) -> bool:
    username = username.strip().lower()
    users    = _load()
    if username not in users:
        return False
    favs = users[username].setdefault("favorite_cities", [])
    if city not in favs and len(favs) < 10:
        favs.append(city)
        _save(users)
    return True


def remove_favorite_city(username: str, city: str) -> bool:
    username = username.strip().lower()
    users    = _load()
    if username not in users:
        return False
    favs = users[username].setdefault("favorite_cities", [])
    if city in favs:
        favs.remove(city)
        _save(users)
    return True


def get_favorites(username: str) -> list[str]:
    data = get_user_data(username)
    return data.get("favorite_cities", []) if data else []


def add_search_history(username: str, city: str) -> None:
    username = username.strip().lower()
    users    = _load()
    if username not in users:
        return
    history = users[username].setdefault("search_history", [])
    history.insert(0, {"city": city, "time": datetime.now().isoformat()})
    users[username]["search_history"] = history[:20]
    _save(users)


def get_search_history(username: str) -> list[dict]:
    data = get_user_data(username)
    return data.get("search_history", []) if data else []
