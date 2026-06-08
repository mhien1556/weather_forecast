"""Cache chung cho toàn app — TTL 10 phút."""
import time

_store: dict = {}
_TTL = 600  # 10 phút


def get(key: str):
    entry = _store.get(key)
    if entry and time.time() - entry['ts'] < _TTL:
        return entry['data']
    return None


def set(key: str, data):
    _store[key] = {'data': data, 'ts': time.time()}


def invalidate(key: str):
    _store.pop(key, None)