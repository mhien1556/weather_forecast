# D:\WeatherForecast\src\features\scheduler_task.py
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

def send_daily_report_job():
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    today_str = now.strftime('%Y-%m-%d')

    pending = get_users_pending_daily_report(current_hour, current_minute, today_str)
    for username, city, _ in pending:
        try:
            weather = get_data(API_KEY, city)
            temp = weather['main']['temp']
            desc = weather['weather'][0]['description']
            content = f"☀️ Báo cáo thời tiết hàng ngày ({city}): {desc}, nhiệt độ {temp}°C."
            save_notification_history(username, content)
            mark_daily_sent(username, today_str)
            logger.info(f"Đã gửi báo cáo cho {username} lúc {now.strftime('%H:%M')}")
        except Exception as e:
            logger.error(f"Lỗi gửi báo cáo cho {username}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_report_job, 'cron', minute='*')
    scheduler.start()
    logger.info("Scheduler daily report đã khởi động")