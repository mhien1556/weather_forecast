from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

from src.database.user_store import (
    get_users_pending_daily_report,
    save_notification_history,
    mark_daily_sent,
)
from src.features.weather.home.service import get_data
from src.common.config import API_KEY

logger = logging.getLogger(__name__)

def start_scheduler():
    pass # Đã gỡ bỏ tính năng thông báo