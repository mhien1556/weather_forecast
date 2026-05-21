from .home import register as register_home
from .forecast import register as register_forecast
from .map import register as register_map
from .analysis import register as register_analysis
from .settings import register as register_settings
from .login import register as register_login
from .profile import register as register_profile

def register_all():
    register_home()
    register_forecast()
    register_map()
    register_analysis()
    register_settings()
    register_login()
    register_profile()
