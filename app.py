import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(__file__))
from src.fetch import get_current_weather, get_forecast_5days
from src.process import parse_current, parse_forecast

st.set_page_config(
    page_title="Dự báo thời tiết",
    page_icon="🌤️",
    layout="wide"
)

st.markdown("# 🌤️ Dự Báo Thời Tiết")
st.markdown("Nhập tên thành phố để xem thời tiết hiện tại và dự báo 5 ngày tới.")
st.divider()

city = st.text_input(
    "🔍 Nhập tên thành phố:",
    placeholder="Ví dụ: Ho Chi Minh City, Hanoi, Da Nang...",
)

if city:
    try:
        with st.spinner("Đang tải dữ liệu..."):
            current_data = get_current_weather(city)
            forecast_data = get_forecast_5days(city)

        current = parse_current(current_data)
        df = parse_forecast(forecast_data)

        icon_url = f"https://openweathermap.org/img/wn/{current['icon']}@2x.png"

        col_icon, col_info = st.columns([1, 4])
        with col_icon:
            st.image(icon_url, width=100)
        with col_info:
            st.markdown(f"## 📍 {current['city']}, {current['country']}")
            st.markdown(f"_{current['description'].capitalize()}_")

        st.markdown("### Thông số hiện tại")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🌡️ Nhiệt độ", f"{current['temp']}°C", f"Cảm giác {current['feels_like']}°C")
        c2.metric("🔼 Cao nhất", f"{current['temp_max']}°C")
        c3.metric("🔽 Thấp nhất", f"{current['temp_min']}°C")
        c4.metric("💧 Độ ẩm", f"{current['humidity']}%")
        c5.metric("💨 Gió", f"{current['wind_speed']} m/s")

        st.divider()
        st.markdown("### 📅 Dự báo 5 ngày tới")

        tab1, tab2 = st.tabs(["🌡️ Nhiệt độ", "💧 Độ ẩm"])

        with tab1:
            fig1 = px.line(
                df, x="datetime", y="temp",
                title="Biểu đồ nhiệt độ (°C)",
                labels={"datetime": "Thời gian", "temp": "Nhiệt độ (°C)"},
                markers=True,
                color_discrete_sequence=["#2E86AB"]
            )
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = px.bar(
                df, x="datetime", y="humidity",
                title="Độ ẩm theo thời gian (%)",
                labels={"datetime": "Thời gian", "humidity": "Độ ẩm (%)"},
                color_discrete_sequence=["#17BEBB"]
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        with st.expander("📊 Xem bảng dữ liệu chi tiết"):
            st.dataframe(
                df[["datetime", "temp", "feels_like", "humidity", "wind_speed", "description"]].rename(columns={
                    "datetime": "Thời gian",
                    "temp": "Nhiệt độ (°C)",
                    "feels_like": "Cảm giác (°C)",
                    "humidity": "Độ ẩm (%)",
                    "wind_speed": "Gió (m/s)",
                    "description": "Mô tả",
                }),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Không tìm thấy thành phố hoặc lỗi kết nối: {e}")
        st.info("💡 Thử nhập tên thành phố bằng tiếng Anh, ví dụ: Ho Chi Minh City")

else:
    st.info("👆 Nhập tên thành phố vào ô tìm kiếm để bắt đầu!")