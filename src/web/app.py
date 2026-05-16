import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .utils import get_location_by_ip

# Import modular page controllers
from .pages.home.home import get_home_data
from .pages.forecast.forecast import get_forecast_data
from .pages.analysis.analysis import get_analysis_data
from .pages.map.map import get_map_data
from .pages.auth.auth import handle_login, handle_register

load_dotenv()

def create_app():
    # We update the template folder to the root of the web directory
    # so we can access pages/home/index.html etc.
    app = Flask(
        __name__,
        template_folder=".",  # This allows us to point to 'pages/home/index.html'
        static_folder="static",
        static_url_path="/static",
    )
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    CORS(app)

    from flask import session

    @app.context_processor
    def inject_user():
        return dict(current_user=session.get("user"))

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    def get_current_city():
        # 1. Ưu tiên city từ URL query (?city=...)
        city = request.args.get("city")
        if city:
            session["current_city"] = city
            return city
        
        # 2. Nếu không có, lấy từ session (đã lưu từ lần trước)
        if "current_city" in session:
            return session["current_city"]
            
        # 3. Nếu mới vào lần đầu, tự động định vị theo IP
        detected_city = get_location_by_ip()
        session["current_city"] = detected_city
        return detected_city

    # ── Trang HTML Modular ──────────────────────────────────────────────────
    @app.route("/")
    def index():
        city = get_current_city()
        weather = get_home_data(API_KEY, city=city)
        return render_template("pages/home/index.html", weather=weather, api_key=API_KEY)

    @app.route("/forecast")
    def forecast():
        city = get_current_city()
        weather = get_forecast_data(API_KEY, city=city)
        return render_template("pages/forecast/forecast.html", weather=weather)

    @app.route("/map")
    def map_page():
        city = get_current_city()
        weather = get_map_data(API_KEY, city=city)
        return render_template("pages/map/map.html", weather=weather, api_key=API_KEY)

    @app.route("/analysis")
    def analysis():
        city = get_current_city()
        weather = get_analysis_data(API_KEY, city=city)
        return render_template("pages/analysis/analysis.html", weather=weather)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if handle_login(username, password):
                session["user"] = {"username": username, "name": "Minh Hiển"} # Mock user data
                return jsonify({"status": "success", "message": "Logged in"})
        return render_template("pages/auth/login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            if handle_register(username, email, password):
                session["user"] = {"username": username, "name": username}
                return jsonify({"status": "success", "message": "Registered"})
        return render_template("pages/auth/register.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return jsonify({"status": "success", "message": "Logged out"})

    return app
