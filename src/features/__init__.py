from .weather.home import register as register_home
from .weather.forecast import register as register_forecast
from .weather.map import register as register_map
from .weather.analysis import register as register_analysis
from .user_management.settings import register as register_settings
from .user_management.login import register as register_login
from .user_management.profile import register as register_profile

def register_all():
    register_home()
    register_forecast()
    register_map()
    register_analysis()
    register_settings()
    register_login()
    register_profile()
