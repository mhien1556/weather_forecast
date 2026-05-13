"""
WeatherNow — main Streamlit application.
"""

from __future__ import annotations

import sys
import os
import base64

# Ensure project root is always on the path (fixes import issues when
# Streamlit is launched from a different working directory).
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from src.fetch   import get_current_weather, get_forecast_5days, get_air_quality, get_uv_index
from src.process import parse_current, parse_forecast, get_daily_summary, parse_aqi, uv_category
from src.auth    import (
    register_user, login_user,
    add_favorite_city, remove_favorite_city, get_favorites,
    add_search_history, get_search_history,
    get_user_data, update_user_profile,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="WeatherNow",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ═══════════════════════════════════════════════════════════════════════════════
_DEFAULTS = {
    "username":     "",
    "display_name": "",
    "avatar":       "🙂",
    "page":         "weather",
    "unit":         "°C",
    "theme_mode":   "dark",
    "bg_style":     "Cloud Sky",
    "accent_color": "#00dbe7",
    "glass_blur":   24,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ═══════════════════════════════════════════════════════════════════════════════
# THEME PRESETS
# ═══════════════════════════════════════════════════════════════════════════════
def _cloud_background_css() -> str:
    """
    Prefer user-provided local cloud image, fallback to online image.
    Returns a valid CSS background value.
    """
    candidates = [
        r"C:\Users\USER\.cursor\projects\d-weather-forecast-weather-forecast1-weather-forecast\assets\c__Users_USER_AppData_Roaming_Cursor_User_workspaceStorage_c6229f5bd6548c85944fc2013977ecbf_images_image-abstract-artistic-soft-pastel-colorful-cloud-sky-background-backdrop-use_1028938-243104-f646f1ff-9540-4390-b137-48372cddf8fe.png",
        os.path.join(_ROOT, "assets", "cloud_bg.png"),
        os.path.join(_ROOT, "assets", "cloud_bg.jpg"),
        r"C:\Users\USER\.cursor\projects\d-weather-forecast-weather-forecast1-weather-forecast\assets\c__Users_USER_AppData_Roaming_Cursor_User_workspaceStorage_c6229f5bd6548c85944fc2013977ecbf_images_image-d6fcafe6-1f07-4a64-88ae-1b415f737107.png",
    ]
    for img_path in candidates:
        if os.path.exists(img_path):
            try:
                ext = os.path.splitext(img_path)[1].lower()
                mime = "image/png" if ext == ".png" else "image/jpeg"
                with open(img_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                return f"url('data:{mime};base64,{data}') center / cover no-repeat fixed"
            except Exception:
                continue
    return "url('https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1920&q=80') center / cover no-repeat fixed"


CLOUD_BG = _cloud_background_css()

DARK_PRESETS = {
    "Midnight": "radial-gradient(circle at 50% 50%, #1a1b26 0%, #0f0f13 100%)",
    "Deep Sea": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)",
    "Cyber":    "linear-gradient(135deg, #09090b 0%, #18181b 100%)",
    "Nordic":   "linear-gradient(135deg, #2e3440 0%, #3b4252 100%)",
    "Sunset":   "linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)",
    "Cloud Sky": CLOUD_BG,
}
LIGHT_PRESETS = {
    "Clean White": "#ffffff",
    "Soft Gray":   "#f8f9fa",
    "Light Blue":  "#e3f2fd",
    "Light Green": "#e8f5e9",
    "Cream":       "#fffef0",
    "Cloud Sky": CLOUD_BG,
}

_is_dark  = st.session_state.theme_mode == "dark"
BG_PRESETS = DARK_PRESETS if _is_dark else LIGHT_PRESETS

_default_bg = "Cloud Sky"
if st.session_state.bg_style not in BG_PRESETS:
    st.session_state.bg_style = _default_bg

current_bg = BG_PRESETS[st.session_state.bg_style]
accent     = st.session_state.accent_color
blur       = st.session_state.glass_blur

if _is_dark:
    text_color    = "#e1e1e6"
    text_sec      = "#94a3b8"
    glass_bg      = "rgba(255,255,255,0.03)"
    glass_border  = "rgba(255,255,255,0.1)"
    navbar_bg     = "rgba(15,15,19,0.8)"
    navbar_border = "rgba(255,255,255,0.05)"
else:
    text_color    = "#1f2937"
    text_sec      = "#6b7280"
    glass_bg      = "rgba(255,255,255,0.8)"
    glass_border  = "#e5e7eb"
    navbar_bg     = "rgba(255,255,255,0.9)"
    navbar_border = "#e5e7eb"


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

html, body, [class*="css"] {{ font-family: 'Geist', 'Inter', sans-serif; }}
#MainMenu, footer, header {{ visibility: hidden; }}

.stApp {{
    background: {current_bg};
    color: {text_color};
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.block-container {{
    max-width: 1120px !important;
    padding-top: 0.65rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 1rem !important;
}}
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(18,20,20,0.45);
    z-index: 0;
    pointer-events: none;
}}

:root {{
    --primary:      {accent};
    --secondary:    #74f5ff;
    --accent-warm:  #ffb68d;
    --text:         {text_color};
    --text-sec:     {text_sec};
    --text-muted:   {text_sec}aa;
    --glass-bg:     {glass_bg};
    --glass-border: {glass_border};
    --error:        #ffb4ab;
    --blur:         {blur}px;
}}

.material-symbols-outlined {{
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}}

/* -- PANELS -- */
.glass-panel, .glass-card {{
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    background: rgba(8, 14, 20, 0.64);
    border-color: rgba(178, 197, 219, 0.13);
}}
.glass-panel:hover, .glass-card:hover {{
    background: rgba(10, 18, 28, 0.72);
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
}}

/* -- NAVBAR -- */
.navbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 10px 18px;
    background: rgba(8, 12, 18, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: sticky;
    top: 0;
    z-index: 1000;
    margin: -0.65rem -1rem 0.35rem -1rem;
    box-shadow: 0 8px 22px rgba(0,0,0,0.28);
}}
.navbar .logo {{ font-size:1.7rem; font-weight:700; color:#e9edf5; letter-spacing:-0.02em; min-width:190px; }}
.navbar .menu {{ flex: 1; display:flex; align-items:center; gap:20px; justify-content:flex-start; }}
.navbar .menu-item {{ color:#b6bfcc; font-size:0.98rem; font-weight:600; text-decoration:none; padding:7px 0; }}
.navbar .menu-item.active {{ color:#14d9ff; border-bottom:2px solid #14d9ff; }}
.navbar .right-tools {{ display:flex; align-items:center; gap:12px; color:#c0cad9; }}
.navbar .tool-icon {{ font-size:16px; opacity:0.9; }}
.avatar-header-popover {{
    position: fixed;
    top: 9px;
    right: 8px;
    z-index: 1201;
}}
.avatar-header-popover .stPopover > button {{
    width: 78px !important;
    height: 36px !important;
    min-height: 36px !important;
    border-radius: 10px !important;
    padding: 0 10px !important;
    background: rgba(255,255,255,0.08) !important;
    color: #e8edf7 !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}}

/* -- HERO -- */
.hero {{ display:none; }}
.hero h1 {{ font-size:1.3rem; font-weight:650; color:#dfe6f2; margin:0; letter-spacing:-0.01em; }}
.hero p  {{ color:#99a4b5; font-size:0.82rem; margin-top:2px; }}

/* -- HERO WEATHER -- */
.hero-weather {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px;
    background: rgba(9, 15, 22, 0.56);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(175, 193, 214, 0.16);
    border-radius: 12px;
    margin-bottom: 12px;
}}
.temp-big   {{ font-size:5rem; font-weight:700; color:white; line-height:1; letter-spacing:-0.04em; }}
.temp-feels {{ color:var(--text-sec); font-size:1.2rem; margin-top:4px; }}

/* -- BENTO GRID -- */
.bento-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(112px,1fr)); gap:8px; margin-bottom:12px; }}
.bento-item {{
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    padding: 12px;
    transition: all 0.3s;
}}
.bento-item:hover   {{ background:rgba(255,255,255,0.08); }}
.bento-icon         {{ color:var(--secondary); margin-bottom:8px; font-size:17px; }}
.bento-label        {{ font-size:12px; letter-spacing:0.1em; font-weight:600; text-transform:uppercase; color:var(--text-muted); margin-bottom:4px; }}
.bento-value        {{ font-size:20px; font-weight:600; color:#e2e2e2; }}

/* -- HOURLY STRIP -- */
.hourly-strip {{
    display: flex !important;
    gap: 12px;
    overflow-x: auto;
    padding: 12px 0;
    scrollbar-width: thin;
    scrollbar-color: rgba(116,245,255,0.2) rgba(255,255,255,0.05);
}}
.hourly-strip::-webkit-scrollbar       {{ height:4px; }}
.hourly-strip::-webkit-scrollbar-track {{ background:rgba(255,255,255,0.05); }}
.hourly-strip::-webkit-scrollbar-thumb {{ background:rgba(116,245,255,0.2); border-radius:10px; }}
.hour-chip {{
    min-width: 78px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 10px 8px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    transition: all 0.3s;
    flex: 0 0 auto;
}}
.hour-chip:hover {{ background:rgba(255,255,255,0.08); }}
.hour-label      {{ font-size:10px; letter-spacing:0.05em; font-weight:600; text-transform:uppercase; color:var(--text-muted); }}
.hour-temp       {{ font-size:20px; font-weight:600; color:#e2e2e2; }}
.hour-rain       {{ font-size:10px; color:var(--secondary); }}
.hour-rain.high  {{ color:var(--error); }}

/* -- DAY STRIP -- */
.day-strip {{ display:flex !important; flex-direction:column !important; gap:8px; }}
.day-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 12px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    transition: all 0.3s;
}}
.day-row:hover    {{ background:rgba(255,255,255,0.08); }}
.day-name         {{ width:80px; font-weight:600; color:#e2e2e2; }}
.day-temps        {{ display:flex; gap:16px; align-items:center; }}
.day-temps .hi    {{ font-weight:600; color:#e2e2e2; }}
.day-temps .lo    {{ color:var(--text-muted); }}

/* -- AQI -- */
.aqi-ring {{
    width:96px; height:96px;
    border-radius:50%;
    border: 8px solid rgba(0,219,231,0.2);
    display:flex; align-items:center; justify-content:center;
    position:relative;
}}
.aqi-ring::before {{
    content:''; position:absolute; inset:-8px;
    border-radius:50%;
    border-top: 8px solid var(--primary);
    box-shadow: 0 0 15px rgba(0,219,231,0.5);
}}
.aqi-value {{ font-size:2.5rem; font-weight:700; color:white; }}

/* -- FAVORITES -- */
.fav-item {{
    display:flex; align-items:center; justify-content:space-between;
    padding:16px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    transition: all 0.3s;
    margin-bottom: 8px;
}}
.fav-item:hover {{ background:rgba(255,255,255,0.08); }}

/* -- STREAMLIT OVERRIDES -- */
[data-testid="metric-container"] {{
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    backdrop-filter: blur(24px) !important;
}}
[data-testid="metric-container"] label {{
    color: var(--text-muted) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: #e2e2e2 !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}}

.stButton > button {{
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    color: #e2e2e2 !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(12px) !important;
}}
.stButton > button:hover {{
    background: rgba(0,219,231,0.15) !important;
    border-color: var(--primary) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(0,219,231,0.2) !important;
    transform: translateY(-1px) !important;
}}
.stButton > button[kind="primary"] {{
    background: rgba(0,219,231,0.2) !important;
    border: 1px solid var(--primary) !important;
    color: white !important;
}}

.stTextInput input, .stPasswordInput input {{
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
    padding: 12px 14px !important;
    transition: all 0.3s ease !important;
}}
.stTextInput input:focus, .stPasswordInput input:focus {{
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(0,219,231,0.15) !important;
}}
.stTextInput > label, .stPasswordInput > label {{ color:#e2e2e2 !important; font-weight:600 !important; }}

.stTabs [data-baseweb="tab-list"] {{ gap:8px; }}
.stTabs [data-baseweb="tab"] {{
    background: var(--glass-bg);
    border-radius: 10px;
    color: var(--text-sec);
    border: 1px solid var(--glass-border);
    padding: 10px 16px !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(0,219,231,0.2) !important;
    color: var(--primary) !important;
    border-color: var(--primary) !important;
}}

.badge {{ padding:6px 12px; border-radius:8px; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }}
.streamlit-expanderHeader, details > summary {{ color:#e2e2e2 !important; }}

/* -- FOOTER -- */
.footer {{
    background: rgba(8, 12, 18, 0.9);
    border-top: 1px solid rgba(255,255,255,0.08);
    padding: 20px 0;
    text-align: left;
    margin-top: 32px;
}}
.footer-brand {{ font-size:1.65rem; font-weight:700; color:#e4e8ef; margin-bottom:8px; }}
.footer-copy  {{ font-size:12px; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-muted); }}
.stPlotlyChart {{
    border-radius: 8px;
    overflow: hidden;
}}
</style>
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
WEEKDAY_VI = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
AVATAR_OPTIONS = ["🙂", "😎", "🧑‍💻", "👩‍💼", "🧑‍🚀", "🌤️", "🔥", "⭐"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Geist, Inter", color="#c7c6cc"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
)


def fmt_temp(temp_c: float) -> str:
    if st.session_state.unit == "°F":
        return str(round(temp_c * 9 / 5 + 32))
    return str(round(temp_c))


def _weather_icon(icon_code: str) -> tuple[str, str]:
    """Map OWM icon code → (material-symbol, color)."""
    if "11" in icon_code:
        return "thunderstorm", "#ffb4ab"
    if "09" in icon_code or "10" in icon_code:
        return "rainy", "#ffb4ab"
    if "13" in icon_code:
        return "cloudy_snowing", "#74f5ff"
    if any(x in icon_code for x in ("02", "03", "04")):
        return "cloud", "#74f5ff"
    if "01n" in icon_code:
        return "nights_stay", "#74f5ff"
    return "wb_sunny", "#74f5ff"


def _desc_to_icon(desc: str) -> str:
    d = desc.lower()
    if "thunderstorm" in d or "sấm" in d:
        return "thunderstorm"
    if "rain" in d or "mưa" in d:
        return "rainy"
    if "snow" in d or "tuyết" in d:
        return "cloudy_snowing"
    if "cloud" in d or "mây" in d:
        return "cloud"
    return "wb_sunny"


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CUSTOMIZER
# ═══════════════════════════════════════════════════════════════════════════════
def show_customizer() -> None:
    with st.sidebar:
        st.markdown("### 🎨 Tùy chỉnh giao diện")

        with st.expander("🌓 Chế độ", expanded=True):
            theme_choice = st.radio(
                "Chế độ giao diện",
                ["☀️ Sáng", "🌙 Tối"],
                index=0 if st.session_state.theme_mode == "light" else 1,
            )
            st.session_state.theme_mode = "light" if theme_choice == "☀️ Sáng" else "dark"

        with st.expander("✨ Nền & Phong cách", expanded=True):
            presets = LIGHT_PRESETS if st.session_state.theme_mode == "light" else DARK_PRESETS
            preset_keys = list(presets.keys())
            current_style = st.session_state.bg_style if st.session_state.bg_style in presets else preset_keys[0]
            st.session_state.bg_style = st.selectbox("Phong cách nền", preset_keys,
                                                      index=preset_keys.index(current_style))
            st.session_state.accent_color = st.color_picker("Màu chủ đạo", st.session_state.accent_color)
            st.session_state.glass_blur   = st.slider("Độ mờ (Blur)", 0, 40, st.session_state.glass_blur)

        with st.expander("⚙️ Hệ thống", expanded=False):
            st.session_state.unit = st.radio(
                "Đơn vị nhiệt độ", ["°C", "°F"],
                index=0 if st.session_state.unit == "°C" else 1,
            )
            if st.button("🔄 Reset về mặc định", use_container_width=True):
                for k, v in _DEFAULTS.items():
                    st.session_state[k] = v
                st.rerun()

        st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH PAGES
# ═══════════════════════════════════════════════════════════════════════════════
def show_login_page() -> None:
    st.markdown("""
    <div class='hero'>
        <h1>🌤️ WeatherNow</h1>
        <p>Hệ thống dự báo thời tiết thông minh · AI Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔐 Đăng nhập")
        u = st.text_input("Tên đăng nhập", key="lu", placeholder="username")
        p = st.text_input("Mật khẩu", type="password", key="lp", placeholder="••••••")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Đăng nhập", use_container_width=True, type="primary"):
                if u and p:
                    ok, msg, data = login_user(u, p)
                    if ok:
                        st.session_state.update(
                            username=u.strip().lower(),
                            display_name=data.get("display_name", u),
                            avatar=data.get("avatar", "🙂"),
                            page="weather",
                        )
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Nhập đầy đủ thông tin.")
        with c2:
            if st.button("📝 Tạo tài khoản", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("👤 Dùng thử không cần đăng nhập", use_container_width=True):
            st.session_state.update(username="__guest__", display_name="Khách", avatar="🙂", page="weather")
            st.rerun()


def show_register_page() -> None:
    st.markdown("""
    <div class='hero'>
        <h1>🌤️ WeatherNow</h1>
        <p>Khởi tạo trải nghiệm cá nhân hóa của bạn</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Đăng ký")
        dn  = st.text_input("Tên hiển thị",        key="rd",  placeholder="Nguyễn Văn A")
        u   = st.text_input("Tên đăng nhập",       key="ru",  placeholder="≥ 3 ký tự")
        p   = st.text_input("Mật khẩu",            key="rp",  type="password", placeholder="≥ 6 ký tự")
        p2  = st.text_input("Xác nhận mật khẩu",   key="rp2", type="password", placeholder="••••••")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Đăng ký", use_container_width=True, type="primary"):
                if p != p2:
                    st.error("Mật khẩu không khớp.")
                elif u and p:
                    ok, msg = register_user(u, p, dn)
                    if ok:
                        st.success(msg)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Nhập đầy đủ thông tin.")
        with c2:
            if st.button("← Quay lại", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# WEATHER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def show_weather_page() -> None:
    is_guest = (not st.session_state.username) or st.session_state.username == "__guest__"
    if is_guest and not st.session_state.display_name:
        st.session_state.display_name = "Khách"
    if is_guest:
        st.session_state.avatar = "🙂"
    else:
        current_user = get_user_data(st.session_state.username) or {}
        st.session_state.avatar = current_user.get("avatar", st.session_state.get("avatar", "🙂"))
    user_favs = [] if is_guest else get_favorites(st.session_state.username)

    # Navbar
    st.markdown(f"""
    <div class='navbar'>
        <div class='logo'>WeatherNow</div>
        <div class='menu'>
            <span class='menu-item active'>Trang chủ</span>
            <span class='menu-item'>Dự báo</span>
            <span class='menu-item'>Bản đồ</span>
            <span class='menu-item'>Phân tích</span>
            <span class='menu-item'>Yêu thích</span>
            <span class='menu-item'>Giới thiệu</span>
        </div>
        <div class='right-tools'>
            <span class='tool-icon'>🔔</span>
            <span class='tool-icon'>⚙️</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not is_guest:
        st.markdown("<div class='avatar-header-popover'>", unsafe_allow_html=True)
        with st.popover(f"{st.session_state.avatar} ⌄", use_container_width=False):
            st.markdown(f"**{st.session_state.display_name}**")
            chosen_avatar = st.selectbox(
                "Ảnh đại diện",
                AVATAR_OPTIONS,
                index=AVATAR_OPTIONS.index(st.session_state.avatar) if st.session_state.avatar in AVATAR_OPTIONS else 0,
                key="header_avatar_choice",
            )
            if chosen_avatar != st.session_state.avatar:
                ok, msg = update_user_profile(st.session_state.username, avatar=chosen_avatar)
                if ok:
                    st.session_state.avatar = chosen_avatar
                    st.success("Đã cập nhật avatar.")
                    st.rerun()
                else:
                    st.error(msg)
            if st.button("👤 Hồ sơ", key="profile_top_btn", use_container_width=True):
                st.session_state.page = "profile"
                st.rerun()
            if st.button("🚪 Đăng xuất", key="auth_top_btn", use_container_width=True):
                st.session_state.update(username="", display_name="", avatar="🙂", page="login")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class='hero'>
        <h1>Thời tiết realtime, trực quan và hiện đại</h1>
        <p>Dữ liệu theo giờ · AQI · UV · Radar</p>
    </div>
    """, unsafe_allow_html=True)

    if is_guest:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### 👋 Bạn đang ở chế độ khách")
        st.caption("Đăng nhập hoặc đăng ký để lưu thành phố yêu thích, lịch sử tìm kiếm và hồ sơ cá nhân.")
        g1, g2 = st.columns(2)
        with g1:
            if st.button("🔐 Đăng nhập", key="guest_to_login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with g2:
            if st.button("📝 Đăng ký", key="guest_to_register", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Search bar + quick buttons
    QUICK = user_favs[:5] if user_favs else ["Ho Chi Minh City", "Hanoi", "Da Nang", "Can Tho", "Hue"]
    sc, *qcols = st.columns([2] + [1] * len(QUICK))
    with sc:
        city_input = st.text_input("🔍", placeholder="Tìm kiếm thành phố...", label_visibility="collapsed")
    city = city_input
    for i, qc in enumerate(QUICK):
        with qcols[i]:
            if st.button(f"📍 {qc}", key=f"q{i}", use_container_width=True):
                city = qc

    if not city:
        if not is_guest:
            hist = get_search_history(st.session_state.username)
            if hist:
                st.markdown("#### 🕐 Tìm kiếm gần đây")
                hcols = st.columns(min(len(hist), 5))
                for i, h in enumerate(hist[:5]):
                    with hcols[i]:
                        if st.button(h["city"], key=f"h{i}", use_container_width=True):
                            city = h["city"]
        if not city:
            st.markdown(
                "<div style='text-align:center;padding:3rem;color:#999;'>"
                "<p style='font-size:3rem;'>🌍</p><p>Nhập tên thành phố để bắt đầu</p></div>",
                unsafe_allow_html=True,
            )
            st.stop()

    if not is_guest:
        add_search_history(st.session_state.username, city)

    # -- Fetch --
    try:
        with st.spinner("⚡ Đang tải..."):
            raw_cur = get_current_weather(city)
            raw_fc  = get_forecast_5days(city)
        cur   = parse_current(raw_cur)
        df    = parse_forecast(raw_fc)
        daily = get_daily_summary(df)
        lat, lon = cur["lat"], cur["lon"]
        aqi_data = parse_aqi(get_air_quality(lat, lon))
        uvi      = get_uv_index(lat, lon)
        uv_lab, uv_col = uv_category(uvi)
    except Exception as e:
        st.error(f"❌ Không tìm thấy '{city}' hoặc lỗi kết nối.")
        st.info("💡 Thử: **Ho Chi Minh City**, **Hanoi**, **Da Nang**")
        with st.expander("🔧 Chi tiết lỗi"):
            st.code(str(e))
        return

    # -- Hero weather card --
    now         = datetime.now()
    date_str    = f"{WEEKDAY_VI[now.weekday()]}, {now.day} Tháng {now.month}"
    mat_icon    = _desc_to_icon(cur["description"])
    sunrise_str = datetime.fromtimestamp(cur["sunrise"]).strftime("%H:%M") if cur.get("sunrise") else "--:--"
    sunset_str  = datetime.fromtimestamp(cur["sunset"]).strftime("%H:%M")  if cur.get("sunset")  else "--:--"
    vis_str     = f"{cur['visibility'] // 1000}km" if cur.get("visibility") else "N/A"

    st.markdown(f"""
    <div class='hero-weather'>
        <div style='flex:1;'>
            <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px;'>
                <span class='material-symbols-outlined' style='color:#74f5ff;font-size:28px;'>location_on</span>
                <h2 style='margin:0;color:#e2e2e2;font-size:2rem;font-weight:600;letter-spacing:-0.02em;'>
                    {cur['city']}, {cur['country']}</h2>
            </div>
            <p style='margin:0;color:#c7c6cc;font-size:1.1rem;'>{date_str} • {now.strftime('%H:%M')}</p>
        </div>
        <div style='display:flex;align-items:center;gap:16px;'>
            <span class='material-symbols-outlined' style='font-size:4.5rem;color:#ddfcff;'>{mat_icon}</span>
            <div>
                <div class='temp-big'>{fmt_temp(cur['temp'])}{st.session_state.unit}</div>
                <p class='temp-feels' style='text-transform:capitalize;'>
                    {cur['description']} • Cảm giác như {fmt_temp(cur['feels_like'])}°</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not is_guest:
        is_fav = cur["city"] in user_favs
        if st.button(
            "💔 Bỏ yêu thích" if is_fav else "⭐ Thêm yêu thích",
            key="fav_toggle",
        ):
            (remove_favorite_city if is_fav else add_favorite_city)(st.session_state.username, cur["city"])
            st.rerun()

    # -- Bento metrics --
    bento_items = [
        ("humidity_percentage", "Độ ẩm",    f"{cur['humidity']}%"),
        ("air",                 "Gió",       f"{cur['wind_speed']}m/s"),
        ("compress",            "Áp suất",   f"{cur['pressure']}hPa"),
        ("visibility",          "Tầm nhìn",  vis_str),
        ("thermostat_auto",     "Cảm giác",  f"{fmt_temp(cur['feels_like'])}°"),
        ("wb_sunny",            "Bình minh", sunrise_str),
        ("bedtime",             "Hoàng hôn", sunset_str),
        ("cloud",               "Mây",       f"{cur['cloudiness']}%"),
    ]
    bento_html = "<div class='bento-grid'>"
    for icon, label, value in bento_items:
        bento_html += f"""
        <div class='bento-item'>
            <span class='material-symbols-outlined bento-icon'>{icon}</span>
            <div class='bento-label'>{label}</div>
            <div class='bento-value'>{value}</div>
        </div>"""
    bento_html += "</div>"
    st.markdown(bento_html, unsafe_allow_html=True)

    # -- Hourly forecast strip --
    st.markdown("<div class='glass-panel' style='padding:24px 32px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:1.5rem;font-weight:500;margin-bottom:16px;color:#e2e2e2;'>Dự báo theo giờ</h3>",
                unsafe_allow_html=True)
    hourly_html = "<div class='hourly-strip'>"
    for _, row in df.head(12).iterrows():
        h_icon, icon_color = _weather_icon(row["icon"])
        pop = row["pop"]
        if pop > 50:
            icon_color = "#ffb4ab"
        hourly_html += f"""
        <div class='hour-chip'>
            <span class='hour-label'>{row['datetime'].strftime('%H:%M')}</span>
            <span class='material-symbols-outlined' style='color:{icon_color};'>{h_icon}</span>
            <span class='hour-temp'>{fmt_temp(row['temp'])}°</span>
            <span class='hour-rain {"high" if pop > 50 else ""}'>{pop}%</span>
        </div>"""
    hourly_html += "</div>"
    st.markdown(hourly_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -- Two-column layout --
    col_left, col_right = st.columns([8, 4])

    with col_right:
        # AQI card
        if aqi_data:
            aqi_val = aqi_data["aqi"]
            aqi_msg = ("Không khí trong lành." if aqi_val <= 2 else
                       "Chất lượng trung bình." if aqi_val <= 3 else "Không khí kém.")
            st.markdown(f"""
            <div class='glass-panel'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;'>
                    <h3 style='font-size:1.5rem;font-weight:500;margin:0;color:#e2e2e2;'>Chất lượng không khí</h3>
                    <span class='material-symbols-outlined' style='color:#74f5ff;'>info</span>
                </div>
                <div style='display:flex;align-items:center;gap:24px;margin-bottom:24px;'>
                    <div class='aqi-ring'><span class='aqi-value'>{aqi_val}</span></div>
                    <div>
                        <div style='font-size:24px;font-weight:600;color:#00dbe7;'>{aqi_data['label']}</div>
                        <p style='color:#c7c6cc;margin:4px 0 0;font-size:0.9rem;'>{aqi_msg}</p>
                    </div>
                </div>
                <div style='display:flex;flex-direction:column;gap:12px;'>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#909096;'>PM2.5</span>
                        <span style='color:#e2e2e2;'>{aqi_data['pm2_5']} µg/m³</span>
                    </div>
                    <div style='width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:99px;overflow:hidden;'>
                        <div style='width:{min(aqi_data["pm2_5"]/75*100,100):.0f}%;height:100%;background:#00dbe7;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#909096;'>CO</span>
                        <span style='color:#e2e2e2;'>{aqi_data['co']} µg/m³</span>
                    </div>
                    <div style='width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:99px;overflow:hidden;'>
                        <div style='width:{min(aqi_data["co"]/15000*100,100):.0f}%;height:100%;background:#00dbe7;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # UV card
        if uvi is not None:
            uv_advice = (
                "Không cần bảo vệ."          if uvi < 3  else
                "Nên đội mũ."                if uvi < 6  else
                "Kem chống nắng SPF 30+."    if uvi < 8  else
                "⚠️ Hạn chế ra ngoài."       if uvi < 11 else
                "🚨 Rất nguy hiểm!"
            )
            st.markdown(f"""
            <div class='glass-panel'>
                <h3 style='font-size:1.5rem;font-weight:500;margin:0 0 16px;color:#e2e2e2;'>Chỉ số UV</h3>
                <span class='badge' style='background:{uv_col}22;color:{uv_col};border:1px solid {uv_col}44;'>
                    UV {uvi:.1f} – {uv_lab}</span>
                <p style='color:#c7c6cc;font-size:.9rem;margin-top:16px;line-height:1.5;'>{uv_advice}</p>
            </div>
            """, unsafe_allow_html=True)

        # 7-day forecast
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:1.5rem;font-weight:500;margin-bottom:16px;color:#e2e2e2;'>Dự báo 7 ngày</h3>",
                    unsafe_allow_html=True)
        days_html = "<div class='day-strip'>"
        for i, row in daily.iterrows():
            d      = row["date"]
            label  = "Hôm nay" if i == 0 else WEEKDAY_VI[d.weekday()][:5]
            d_icon, d_color = _weather_icon(row["icon"])
            days_html += f"""
            <div class='day-row'>
                <span class='day-name'>{label}</span>
                <span class='material-symbols-outlined' style='color:{d_color};'>{d_icon}</span>
                <div class='day-temps'>
                    <span class='hi'>{fmt_temp(row['temp_max'])}°</span>
                    <span class='lo'>{fmt_temp(row['temp_min'])}°</span>
                </div>
            </div>"""
        days_html += "</div>"
        st.markdown(days_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Favorites
        if not is_guest and user_favs:
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:1.5rem;font-weight:500;margin-bottom:16px;color:#e2e2e2;'>Danh sách yêu thích</h3>",
                        unsafe_allow_html=True)
            for fav_city in user_favs[:5]:
                st.markdown(f"""
                <div class='fav-item'>
                    <p style='font-weight:600;margin:0;color:#e2e2e2;'>{fav_city}</p>
                    <span class='material-symbols-outlined' style='color:#c7c6cc;'>chevron_right</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_left:
        # Analytics charts
        st.markdown("<div class='glass-panel' style='padding:32px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:1.5rem;font-weight:500;margin-bottom:8px;color:#e2e2e2;'>Phân tích dữ liệu</h3>",
                    unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🌡️ Nhiệt độ", "💧 Độ ẩm", "🌧️ Mưa"])

        with t1:
            chart_df = df.copy()
            if st.session_state.unit == "°F":
                for col in ("temp", "temp_min", "temp_max"):
                    chart_df[col] = chart_df[col] * 9 / 5 + 32
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=chart_df["datetime"], y=chart_df["temp_max"], name="Cao nhất",
                                     line=dict(color="#ffb68d", width=2), mode="lines+markers"))
            fig.add_trace(go.Scatter(x=chart_df["datetime"], y=chart_df["temp"], name="Nhiệt độ",
                                     line=dict(color="#00dbe7", width=2.5),
                                     fill="tonexty", fillcolor="rgba(0,219,231,0.08)", mode="lines+markers"))
            fig.add_trace(go.Scatter(x=chart_df["datetime"], y=chart_df["temp_min"], name="Thấp nhất",
                                     line=dict(color="#74f5ff", width=2),
                                     fill="tonexty", fillcolor="rgba(116,245,255,0.06)", mode="lines+markers"))
            fig.update_layout(title=f"Xu hướng Nhiệt độ ({st.session_state.unit})", **CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            fig = go.Figure(go.Scatter(x=df["datetime"], y=df["humidity"], fill="tozeroy",
                                       fillcolor="rgba(0,219,231,0.1)", line=dict(color="#00dbe7", width=2)))
            fig.update_layout(title="Độ ẩm (%)", **CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with t3:
            fig = go.Figure()
            fig.add_bar(x=df["datetime"], y=df["rain_3h"], name="Mưa (mm/3h)", marker_color="#ffb68d")
            fig.add_trace(go.Scatter(x=df["datetime"], y=df["pop"], name="Xác suất (%)", yaxis="y2",
                                     line=dict(color="#00dbe7", width=2)))
            fig.update_layout(
                title="Lượng mưa & Xác suất kết tủa",
                yaxis=dict(**CHART_LAYOUT["yaxis"], title="mm / 3h"),
                yaxis2=dict(title="%", overlaying="y", side="right", range=[0, 100]),
                **{k: v for k, v in CHART_LAYOUT.items() if k != "yaxis"},
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Map
        st.markdown("<div class='glass-panel' style='padding:0;overflow:hidden;border-radius:12px;'>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div style='padding:16px 24px;'>
            <span style='display:inline-flex;align-items:center;gap:8px;background:rgba(18,20,20,0.7);
                padding:6px 16px;border-radius:99px;border:1px solid rgba(255,255,255,0.2);
                font-size:12px;letter-spacing:0.1em;font-weight:600;text-transform:uppercase;color:white;'>
                <span style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></span>
                Radar trực tiếp
            </span>
        </div>
        """, unsafe_allow_html=True)
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
        st.pydeck_chart(
            pdk.Deck(
                map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
                initial_view_state=pdk.ViewState(
                    latitude=lat,
                    longitude=lon,
                    zoom=8.5,
                    pitch=45,
                    bearing=20,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_df,
                        get_position="[lon, lat]",
                        get_fill_color=[0, 219, 231, 220],
                        get_line_color=[255, 255, 255, 220],
                        line_width_min_pixels=2,
                        get_radius=2200,
                        stroked=True,
                        filled=True,
                    ),
                ],
                tooltip={"text": f"{cur['city']}, {cur['country']}"},
            ),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Data table
        with st.expander("📊 Bảng dữ liệu chi tiết"):
            dd = daily.copy()
            dd["date"] = dd["date"].astype(str)
            st.dataframe(
                dd.rename(columns={
                    "date": "Ngày", "temp_min": "Min°C", "temp_max": "Max°C",
                    "temp_avg": "TB°C", "humidity_avg": "Ẩm%",
                    "rain_total": "Mưa mm", "pop_max": "Mưa%", "description": "Mô tả",
                }).drop(columns=["icon"]),
                use_container_width=True,
            )

    # Footer
    st.markdown("""
    <div class='footer'>
        <div class='footer-brand'>WeatherNow</div>
        <p class='footer-copy'>© 2024 WeatherNow Inc. Tất cả quyền được bảo lưu.</p>
        <p style='color:#9098a6;font-size:0.74rem;margin-top:10px;'>
            Tính năng AI · Chính sách bảo mật · Điều khoản sử dụng · Hỗ trợ khách hàng
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def show_profile_page() -> None:
    if st.session_state.username == "__guest__":
        st.session_state.page = "login"
        st.rerun()

    user_data = get_user_data(st.session_state.username)
    if not user_data:
        st.error("Không tìm thấy dữ liệu người dùng.")
        if st.button("Quay lại"):
            st.session_state.page = "weather"
            st.rerun()
        return

    st.markdown("""
    <div class='navbar'>
        <div class='logo'>🌤️ WeatherNow</div>
        <div class='user-info'>👤 Hồ sơ cá nhân</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='hero'><h1>Hồ sơ của bạn</h1>"
                "<p>Quản lý định danh và cài đặt hệ thống</p></div>",
                unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 👤 Thông tin cá nhân")
        st.markdown(f"**Tên đăng nhập:** `{st.session_state.username}`")
        new_dn = st.text_input("Tên hiển thị", value=user_data.get("display_name", ""))
        current_avatar = user_data.get("avatar", "🙂")
        avatar_choice = st.selectbox(
            "Ảnh đại diện",
            AVATAR_OPTIONS,
            index=AVATAR_OPTIONS.index(current_avatar) if current_avatar in AVATAR_OPTIONS else 0,
        )
        st.divider()
        st.markdown("#### 🔒 Đổi mật khẩu")
        new_p  = st.text_input("Mật khẩu mới",          type="password", placeholder="Để trống nếu không đổi")
        new_p2 = st.text_input("Xác nhận mật khẩu mới", type="password", placeholder="••••••")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Lưu thay đổi", use_container_width=True, type="primary"):
                if new_p and new_p != new_p2:
                    st.error("Mật khẩu xác nhận không khớp.")
                else:
                    ok, msg = update_user_profile(
                        st.session_state.username,
                        display_name=new_dn,
                        password=new_p if new_p else None,
                        avatar=avatar_choice,
                    )
                    if ok:
                        st.success(msg)
                        st.session_state.display_name = new_dn
                        st.session_state.avatar = avatar_choice
                    else:
                        st.error(msg)
        with c2:
            if st.button("← Quay lại", use_container_width=True):
                st.session_state.page = "weather"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    created = user_data.get("created_at", "N/A")[:10]
    st.markdown(f"<div style='text-align:center;padding:1.5rem 0;color:#aaa;font-size:.8rem;'>"
                f"Tài khoản được tạo vào: {created}</div>",
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
_is_authed = bool(st.session_state.username)

if st.session_state.page == "weather":
    show_customizer()
    show_weather_page()
elif st.session_state.page == "profile" and _is_authed:
    show_customizer()
    show_profile_page()
elif st.session_state.page == "register":
    show_register_page()
else:
    show_login_page()