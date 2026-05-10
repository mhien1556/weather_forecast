import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from src.fetch import get_current_weather, get_forecast_5days, get_air_quality, get_uv_index
from src.process import parse_current, parse_forecast, get_daily_summary, parse_aqi, uv_category
from src.auth import (register_user, login_user, add_favorite_city,
                      remove_favorite_city, get_favorites, add_search_history,
                      get_search_history, get_user_data, update_user_profile)

st.set_page_config(page_title="WeatherNow", page_icon="🌤️", layout="wide", initial_sidebar_state="collapsed")

for key, val in [
    ("logged_in", False), ("username", ""), ("display_name", ""), ("page", "login"), ("unit", "°C"),
    ("bg_style", "Midnight"), ("accent_color", "#6366f1"), ("glass_blur", 12)
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Dynamic Theme Logic ───────────────────────────────────────────────────────
BG_PRESETS = {
    "Midnight": "radial-gradient(circle at 50% 50%, #1a1b26 0%, #0f0f13 100%)",
    "Deep Sea": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)",
    "Cyber": "linear-gradient(135deg, #09090b 0%, #18181b 100%)",
    "Nordic": "linear-gradient(135deg, #2e3440 0%, #3b4252 100%)",
    "Sunset": "linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)"
}

current_bg = BG_PRESETS.get(st.session_state.bg_style, BG_PRESETS["Midnight"])
accent = st.session_state.accent_color
blur = st.session_state.glass_blur

# ── OpenWeatherMap-style CSS ───────────────────────────────────────────────────
# ── AI-Inspired Glassmorphism CSS ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Outfit',sans-serif;}}
#MainMenu,footer,header{{visibility:hidden;}}
.stApp{{background: {current_bg}; color:#e1e1e6;}}

:root {{
    --primary: {accent};
    --blur: {blur}px;
}}

/* ── Glass Cards ── */
.glass-card{{
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(var(--blur));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.glass-card:hover{{
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--primary);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}}

/* ── Hero & Branding ── */
.hero-ai{{
    padding: 80px 20px;
    text-align: center;
    background: linear-gradient(180deg, {accent}11 0%, transparent 100%);
    border-radius: 0 0 60px 60px;
    margin: -1rem -1rem 2rem -1rem;
}}
.hero-ai h1{{
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #fff 0%, var(--primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}}
.hero-ai p{{color:#94a3b8; font-size:1.1rem; margin-top:12px;}}

/* ── Navbar ── */
.navbar-ai{{
    display:flex; align-items:center; justify-content:space-between; padding:16px 32px;
    background: rgba(15, 15, 19, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: sticky; top: 0; z-index: 1000;
    margin: -1rem -1rem 0 -1rem;
}}
.navbar-ai .logo{{font-size:1.6rem; font-weight:700; color:var(--primary); letter-spacing:-0.5px;}}
.navbar-ai .user-info{{color:#94a3b8; font-size:0.95rem; font-weight:500;}}

/* ── Metrics ── */
[data-testid="metric-container"]{{
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 20px !important;
    padding: 20px !important;
}}
[data-testid="metric-container"] label{{color:#94a3b8 !important; font-size:0.85rem !important;}}
[data-testid="metric-container"] [data-testid="stMetricValue"]{{color:#fff !important; font-size:1.8rem !important; font-weight:700 !important;}}

/* ── Buttons ── */
.stButton>button{{
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #fff !important;
    border-radius: 14px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}}
.stButton>button:hover{{
    background: var(--primary) !important;
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
}}
.stButton>button[kind="primary"]{{
    background: var(--primary) !important;
    border: none !important;
}}

/* ── Inputs ── */
.stTextInput input, .stPasswordInput input{{
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 14px !important;
    color: #fff !important;
}}
.stTextInput input:focus{{border-color:var(--primary) !important; box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{{gap:8px;}}
.stTabs [data-baseweb="tab"]{{
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    color: #94a3b8;
    border: 1px solid rgba(255,255,255,0.05);
}}
.stTabs [aria-selected="true"]{{
    background: var(--primary) !important;
    color: #fff !important;
}}

/* ── Day strip ── */
.day-strip{{
    display: flex !important; 
    flex-direction: row !important;
    gap: 12px; 
    overflow-x: auto; 
    padding: 10px 5px;
    flex-wrap: nowrap !important;
    scrollbar-width: none;
}}
.day-strip::-webkit-scrollbar {{ display: none; }}

.day-chip-ai{{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    min-width: 110px;
    flex: 0 0 auto;
    transition: all 0.3s;
}}
.day-chip-ai.active{{
    background: linear-gradient(135deg, var(--primary) 0%, {accent}aa 100%);
    border-color: var(--primary);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}}
.day-chip-ai .temp{{font-size:1.2rem; font-weight:700;}}
.day-chip-ai .label{{font-size:0.8rem; color:#94a3b8;}}
.day-chip-ai.active .label{{color:rgba(255,255,255,0.8);}}

.badge-ai{{
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#94a3b8"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
)

def show_customizer():
    with st.sidebar:
        st.markdown("### 🎨 Tùy chỉnh giao diện")
        with st.expander("✨ Background & Mood", expanded=True):
            st.session_state.bg_style = st.selectbox("Phong cách nền", list(BG_PRESETS.keys()), index=list(BG_PRESETS.keys()).index(st.session_state.bg_style))
            st.session_state.accent_color = st.color_picker("Màu chủ đạo (Accent)", st.session_state.accent_color)
            st.session_state.glass_blur = st.slider("Độ mờ (Glass Blur)", 0, 40, st.session_state.glass_blur)
        
        with st.expander("⚙️ Hệ thống", expanded=False):
            st.session_state.unit = st.radio("Đơn vị nhiệt độ", ["°C", "°F"], index=0 if st.session_state.unit=="°C" else 1)
            if st.button("Reset về mặc định", width="stretch"):
                st.session_state.update(bg_style="Midnight", accent_color="#6366f1", glass_blur=12, unit="°C")
                st.rerun()
        st.divider()

WEEKDAY_VI = {0:"Thứ Hai",1:"Thứ Ba",2:"Thứ Tư",3:"Thứ Năm",4:"Thứ Sáu",5:"Thứ Bảy",6:"Chủ Nhật"}

def fmt_temp(temp_c: float) -> str:
    """Format temperature based on session state unit."""
    if st.session_state.unit == "°F":
        return f"{round(temp_c * 9/5 + 32)}"
    return f"{round(temp_c)}"


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════════════════════

def show_login_page():
    st.markdown("""
    <div class='hero-ai'>
        <h1>🌤️ WeatherNow</h1>
        <p>Hệ thống dự báo thời tiết thông minh · AI Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔐 Đăng nhập")
        u = st.text_input("Tên đăng nhập", key="lu", placeholder="username")
        p = st.text_input("Mật khẩu", type="password", key="lp", placeholder="••••••")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("🚀 Đăng nhập", width="stretch", type="primary"):
                if u and p:
                    ok,msg,data = login_user(u,p)
                    if ok:
                        st.session_state.update(logged_in=True, username=u.strip().lower(),
                                                display_name=data.get("display_name",u), page="weather")
                        st.rerun()
                    else: st.error(msg)
                else: st.warning("Nhập đầy đủ thông tin.")
        with c2:
            if st.button("📝 Tạo tài khoản", width="stretch"):
                st.session_state.page="register"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("👤 Dùng thử không cần đăng nhập", width="stretch"):
            st.session_state.update(username="__guest__", display_name="Khách", page="weather"); st.rerun()


def show_register_page():
    st.markdown("<div class='hero-ai'><h1>🌤️ WeatherNow</h1><p>Khởi tạo trải nghiệm cá nhân hóa của bạn</p></div>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Đăng ký")
        dn = st.text_input("Tên hiển thị", key="rd", placeholder="Nguyễn Văn A")
        u = st.text_input("Tên đăng nhập", key="ru", placeholder="≥ 3 ký tự")
        p = st.text_input("Mật khẩu", type="password", key="rp", placeholder="≥ 6 ký tự")
        p2 = st.text_input("Xác nhận", type="password", key="rp2", placeholder="••••••")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("✅ Đăng ký", width="stretch", type="primary"):
                if p!=p2: st.error("Mật khẩu không khớp.")
                elif u and p:
                    ok,msg = register_user(u,p,dn)
                    if ok: st.success(msg); st.session_state.page="login"; st.rerun()
                    else: st.error(msg)
                else: st.warning("Nhập đầy đủ thông tin.")
        with c2:
            if st.button("← Quay lại", width="stretch"):
                st.session_state.page="login"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# WEATHER PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def show_weather_page():
    is_guest = st.session_state.username == "__guest__"
    user_favs = [] if is_guest else get_favorites(st.session_state.username)

    # ── Navbar ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class='navbar-ai'>
        <div class='logo'>🌤️ WeatherNow</div>
        <div class='user-info'>👤 {st.session_state.display_name}</div>
    </div>
    """, unsafe_allow_html=True)

    nb1, nb2, nb3 = st.columns([4,1,1])
    with nb2:
        if not is_guest:
            if st.button("👤 Hồ sơ", width="stretch"):
                st.session_state.page = "profile"
                st.rerun()
    with nb3:
        if st.button("🚪 Đăng xuất" if not is_guest else "🔐 Đăng nhập", width="stretch"):
            st.session_state.update(logged_in=False, username="", display_name="", page="login")
            st.rerun()

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class='hero-ai'>
        <h1>Khám phá thời tiết</h1>
        <p>Phân tích dữ liệu thời gian thực · AQI · UV · Insights</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Search bar ───────────────────────────────────────────────────────────
    QUICK = user_favs[:5] if user_favs else ["Ho Chi Minh City","Hanoi","Da Nang","Can Tho","Hue"]
    sc, *qcols = st.columns([2]+[1]*len(QUICK))
    with sc:
        city_input = st.text_input("🔍", placeholder="Tìm kiếm thành phố...", label_visibility="collapsed")
    city = city_input
    for i,qc in enumerate(QUICK):
        with qcols[i]:
            if st.button(f"📍 {qc}", key=f"q{i}", width="stretch"):
                city = qc

    if not city:
        # History
        if not is_guest:
            hist = get_search_history(st.session_state.username)
            if hist:
                st.markdown("#### 🕐 Tìm kiếm gần đây")
                hcols = st.columns(min(len(hist),5))
                for i,h in enumerate(hist[:5]):
                    with hcols[i]:
                        if st.button(h['city'], key=f"h{i}", width="stretch"): city=h['city']
        if not city:
            st.markdown("<div style='text-align:center;padding:3rem;color:#999;'><p style='font-size:3rem;'>🌍</p>"
                        "<p>Nhập tên thành phố để bắt đầu</p></div>", unsafe_allow_html=True)
            st.stop()

    if not is_guest:
        add_search_history(st.session_state.username, city)

    # ── Fetch ────────────────────────────────────────────────────────────────
    try:
        with st.spinner("⚡ Đang tải..."):
            raw_cur = get_current_weather(city)
            raw_fc = get_forecast_5days(city)
        cur = parse_current(raw_cur)
        df = parse_forecast(raw_fc)
        daily = get_daily_summary(df)
        lat, lon = cur["lat"], cur["lon"]
        raw_aqi = get_air_quality(lat, lon)
        uvi = get_uv_index(lat, lon)
        aqi_data = parse_aqi(raw_aqi)
        uv_lab, uv_col = uv_category(uvi)
    except Exception as e:
        st.error(f"❌ Không tìm thấy '{city}' hoặc lỗi kết nối.")
        st.info("💡 Thử: **Ho Chi Minh City**, **Hanoi**, **Da Nang**")
        with st.expander("🔧 Chi tiết lỗi"): st.code(str(e))
        return

    # ── Location + Current ───────────────────────────────────────────────────
    icon_url = f"https://openweathermap.org/img/wn/{cur['icon']}@4x.png"

    st.markdown(f"""
    <div class='glass-card' style='display:flex;align-items:center;gap:24px;'>
        <img src='{icon_url}' width='120' style='filter: drop-shadow(0 0 15px rgba(99,102,241,0.5));'/>
        <div style='flex:1;'>
            <h2 style='margin:0;color:#fff;font-size:2.2rem;'>📍 {cur['city']}, {cur['country']}</h2>
            <p style='margin:6px 0;color:#94a3b8;text-transform:capitalize;font-weight:500;'>{cur['description']} · {datetime.now().strftime('%H:%M %d/%m/%Y')}</p>
            <div style='display:flex;align-items:baseline;gap:20px;'>
                <span style='font-size:4.5rem;font-weight:700;color:#fff;'>{fmt_temp(cur['temp'])}{st.session_state.unit}</span>
                <span style='color:#94a3b8;font-size:1.1rem;'>Cảm giác {fmt_temp(cur['feels_like'])}° · <span style='color:var(--primary);'>↓{fmt_temp(cur['temp_min'])}° ↑{fmt_temp(cur['temp_max'])}°</span></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Favorite button
    if not is_guest:
        is_fav = cur["city"] in user_favs
        if st.button(f"{'💔 Bỏ yêu thích' if is_fav else '⭐ Thêm yêu thích'}", key="fav_toggle"):
            (remove_favorite_city if is_fav else add_favorite_city)(st.session_state.username, cur["city"])
            st.rerun()

    # ── Day strip (forecast theo ngày) ───────────────────────────────────────
    days_html = ""
    for i, row in daily.iterrows():
        d = row["date"]
        wd = WEEKDAY_VI.get(d.weekday(), "") if hasattr(d, "weekday") else str(d)
        label = "Hôm nay" if i == 0 else wd
        ic = f"https://openweathermap.org/img/wn/{row['icon']}.png"
        days_html += f"""<div class='day-chip-ai {"active" if i==0 else ""}'>
            <div class='label'>{label}</div>
            <img src='{ic}' width='40' style='margin:8px 0;'/>
            <div class='temp'>{fmt_temp(row['temp_max'])}°</div>
            <div class='label'>{fmt_temp(row['temp_min'])}°</div>
        </div>"""

    st.markdown(f"<div class='day-strip'>{days_html}</div>", unsafe_allow_html=True)

    # ── Metrics ──────────────────────────────────────────────────────────────
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("💧 Độ ẩm", f"{cur['humidity']}%")
    m2.metric("💨 Gió", f"{cur['wind_speed']} m/s", cur['wind_dir'])
    m3.metric("🌡️ Áp suất", f"{cur['pressure']} hPa")
    m4.metric("☁️ Mây", f"{cur['cloudiness']}%")
    vis = f"{cur['visibility']//1000} km" if cur['visibility'] else "N/A"
    m5.metric("👁️ Tầm nhìn", vis)
    if aqi_data: m6.metric("🌿 AQI", aqi_data['aqi'], aqi_data['label'])
    elif uvi is not None: m6.metric("☀️ UV", f"{uvi:.1f}", uv_lab)

    # ── AQI + UV cards ───────────────────────────────────────────────────────
    if aqi_data or uvi is not None:
        ca, cb = st.columns(2)
        if aqi_data:
            with ca:
                st.markdown(f"""<div class='glass-card'>
                    <h4 style='color:#fff;margin-bottom:16px;'>🌿 Chất lượng không khí</h4>
                    <span class='badge-ai' style='background:{aqi_data["color"]}22;color:{aqi_data["color"]};border:1px solid {aqi_data["color"]}44;'>
                        AQI {aqi_data["aqi"]} – {aqi_data["label"]}</span>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px;font-size:.9rem;color:#94a3b8;'>
                        <div>PM2.5: <b style='color:#fff;'>{aqi_data['pm2_5']}</b></div><div>PM10: <b style='color:#fff;'>{aqi_data['pm10']}</b></div>
                        <div>O₃: <b style='color:#fff;'>{aqi_data['o3']}</b></div><div>NO₂: <b style='color:#fff;'>{aqi_data['no2']}</b></div>
                    </div></div>""", unsafe_allow_html=True)
        if uvi is not None:
            advice = ('Không cần bảo vệ.' if uvi<3 else 'Nên đội mũ.' if uvi<6 else
                      'Kem chống nắng SPF 30+.' if uvi<8 else '⚠️ Hạn chế ra ngoài.' if uvi<11 else '🚨 Rất nguy hiểm!')
            with cb:
                st.markdown(f"""<div class='glass-card'>
                    <h4 style='color:#fff;margin-bottom:16px;'>☀️ Chỉ số UV</h4>
                    <span class='badge-ai' style='background:{uv_col}22;color:{uv_col};border:1px solid {uv_col}44;'>
                        UV {uvi:.1f} – {uv_lab}</span>
                    <p style='color:#94a3b8;font-size:.9rem;margin-top:20px;line-height:1.5;'>{advice}</p>
                </div>""", unsafe_allow_html=True)

    # ── Map ──────────────────────────────────────────────────────────────────
    st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}), zoom=8, width="stretch")

    # ── Charts ───────────────────────────────────────────────────────────────
    st.markdown("### 📅 Dự báo theo giờ")
    t1,t2,t3 = st.tabs(["🌡️ Nhiệt độ","💧 Độ ẩm","🌧️ Mưa"])

    with t1:
        # Unit conversion for charts
        chart_df = df.copy()
        if st.session_state.unit == "°F":
            for col in ["temp", "temp_min", "temp_max"]:
                chart_df[col] = chart_df[col] * 9/5 + 32

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_df["datetime"],y=chart_df["temp_max"],name="Cao nhất",line=dict(color="#f43f5e",width=2),mode="lines+markers"))
        fig.add_trace(go.Scatter(x=chart_df["datetime"],y=chart_df["temp"],name="Nhiệt độ",line=dict(color="#6366f1",width=2.5),
                                 fill="tonexty",fillcolor="rgba(99, 102, 241, 0.08)",mode="lines+markers"))
        fig.add_trace(go.Scatter(x=chart_df["datetime"],y=chart_df["temp_min"],name="Thấp nhất",line=dict(color="#06b6d4",width=2),
                                 fill="tonexty",fillcolor="rgba(6, 182, 212, 0.08)",mode="lines+markers"))
        fig.update_layout(title=f"Xu hướng Nhiệt độ ({st.session_state.unit})",**CHART_LAYOUT)
        st.plotly_chart(fig,width="stretch")

    with t2:
        fig = go.Figure(go.Scatter(x=df["datetime"],y=df["humidity"],fill="tozeroy",
                                    fillcolor="rgba(6, 182, 212, 0.1)",line=dict(color="#06b6d4",width=2),mode="lines"))
        fig.update_layout(title="Độ ẩm (%)",**CHART_LAYOUT)
        st.plotly_chart(fig,width="stretch")

    with t3:
        fig = go.Figure()
        fig.add_bar(x=df["datetime"],y=df["rain_3h"],name="Mưa (mm/3h)",marker_color="#6366f1")
        fig.add_trace(go.Scatter(x=df["datetime"],y=df["pop"],name="Xác suất (%)",yaxis="y2",line=dict(color="#f43f5e",width=2),mode="lines"))
        rl = {**CHART_LAYOUT}
        rl["yaxis"] = {**CHART_LAYOUT.get("yaxis",{}),"title":"mm / 3h"}
        fig.update_layout(title="Lượng mưa & Xác suất kết tủa",yaxis2=dict(title="%",overlaying="y",side="right",range=[0,100]),**rl)
        st.plotly_chart(fig,width="stretch")

    # ── Daily table ──────────────────────────────────────────────────────────
    with st.expander("📊 Bảng dữ liệu chi tiết"):
        dd = daily.copy()
        dd["date"] = dd["date"].astype(str)
        st.dataframe(dd.rename(columns={"date":"Ngày","temp_min":"Min°C","temp_max":"Max°C",
            "temp_avg":"TB°C","humidity_avg":"Ẩm%","rain_total":"Mưa mm","pop_max":"Mưa%","description":"Mô tả"
        }).drop(columns=["icon"]),width="stretch")

    st.markdown("<div style='text-align:center;padding:1.5rem 0;color:#aaa;font-size:.8rem;'>"
                "Powered by <b>OpenWeatherMap</b> · Built with <b>Streamlit</b> + <b>Plotly</b></div>",
                unsafe_allow_html=True)


def show_profile_page():
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

    st.markdown(f"""
    <div class='navbar-ai'>
        <div class='logo'>🌤️ WeatherNow</div>
        <div class='user-info'>👤 Hồ sơ cá nhân</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='hero-ai'><h1>Hồ sơ của bạn</h1><p>Quản lý định danh và cài đặt hệ thống</p></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"#### 👤 Thông tin cá nhân")
        st.markdown(f"**Tên đăng nhập:** `{st.session_state.username}`")
        
        new_dn = st.text_input("Tên hiển thị", value=user_data.get("display_name", ""))
        
        st.divider()
        st.markdown("#### 🔒 Đổi mật khẩu")
        new_p = st.text_input("Mật khẩu mới", type="password", placeholder="Để trống nếu không đổi")
        new_p2 = st.text_input("Xác nhận mật khẩu mới", type="password", placeholder="••••••")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Lưu thay đổi", width="stretch", type="primary"):
                if new_p and new_p != new_p2:
                    st.error("Mật khẩu xác nhận không khớp.")
                else:
                    ok, msg = update_user_profile(
                        st.session_state.username, 
                        display_name=new_dn, 
                        password=new_p if new_p else None
                    )
                    if ok:
                        st.success(msg)
                        st.session_state.display_name = new_dn
                        # Optional: st.rerun() to refresh
                    else:
                        st.error(msg)
        with c2:
            if st.button("← Quay lại", width="stretch"):
                st.session_state.page = "weather"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;padding:1.5rem 0;color:#aaa;font-size:.8rem;'>"
                "Tài khoản được tạo vào: " + user_data.get("created_at", "N/A")[:10] + "</div>",
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTING
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "weather" and (st.session_state.logged_in or st.session_state.username == "__guest__"):
    show_customizer()
    show_weather_page()
elif st.session_state.page == "profile":
    show_customizer()
    show_profile_page()
elif st.session_state.page == "register":
    show_register_page()
else:
    show_login_page()