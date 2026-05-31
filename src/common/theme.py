"""Giao diện glassmorphism — CSS nhúng qua Python (NiceGUI)."""

STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --primary-bg: #0a0c10;
    --card-bg: rgba(255, 255, 255, 0.05);
    --card-border: rgba(255, 255, 255, 0.1);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.6);
    --accent-color: #4facfe;
    --danger-text: #f87171;
    --success-color: #4ade80;
    --font-main: 'Inter', sans-serif;
    --font-heading: 'Outfit', sans-serif;
}

html, body, .nicegui-content, .q-layout, .q-page, .q-page-container, #app {
    font-family: var(--font-main) !important;
    background-color: var(--primary-bg) !important;
    background: var(--primary-bg) !important;
    color: var(--text-primary) !important;
    margin: 0;
    overflow-x: hidden;
}

.q-card, .q-dialog__inner > .q-card {
    background: rgba(255, 255, 255, 0.04) !important;
    color: #fff !important;
}

.q-field__native, .q-field__label, .q-btn, .q-item__label {
    color: #fff !important;
}

a, .q-link { color: inherit !important; }

.app-container { position: relative; min-height: 100vh; width: 100%; }

.hero-bg {
    position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
    z-index: 0; pointer-events: none;
    background-image: url('/static/images/sunny.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    transition: background-image 0.5s ease-in-out;
}
.hero-bg.rain {
    background-image: url('/static/images/rainy.png');
}
.hero-bg .overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to bottom, rgba(10,12,16,0.2) 0%, rgba(10,12,16,0.92) 100%);
}

div { box-sizing: border-box; }

.page-content { position: relative; z-index: 1; }

.navbar {
    display: flex !important; justify-content: space-between; align-items: center;
    padding: 0.75rem 4%; background: rgba(15,15,20,0.7);
    backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.08);
    position: sticky; top: 0; z-index: 1000;
}
.logo {
    font-family: var(--font-heading); font-size: 1.6rem; font-weight: 700;
    color: #fff !important; text-decoration: none !important; letter-spacing: -0.5px;
}
.nav-links {
    display: flex !important; flex-direction: row !important; flex-wrap: wrap;
    gap: 2rem !important; list-style: none; margin: 0; padding: 0; align-items: center;
}
.nav-left { display: flex !important; align-items: center; gap: 3rem; }
.nav-right { display: flex !important; align-items: center; gap: 1.25rem; }
.nav-search { flex: 1; max-width: 450px; margin: 0 2rem; display: flex !important; align-items: center; gap: 0.5rem; }
.nav-links a, .nav-links .nav-link {
    text-decoration: none !important; color: rgba(255,255,255,0.6) !important;
    font-weight: 600; font-size: 0.95rem; padding: 0.5rem 0; position: relative;
    cursor: pointer;
}
.nav-links a:hover, .nav-links a.active, .nav-links .nav-link:hover, .nav-links .nav-link.active { color: #fff !important; }
.nav-links a.active::after, .nav-links .nav-link.active::after {
    content: ''; position: absolute; bottom: -2px; left: 0; width: 100%; height: 3px;
    background: #4facfe; border-radius: 4px;
}

.content-wrapper {
    max-width: 1400px; margin: 0 auto; padding: 2rem 4%;
    width: 100%; box-sizing: border-box;
}

.city-search-bar-wrap { margin-bottom: 1.5rem; padding-top: 0.5rem; }
.city-search-bar {
    display: flex !important; align-items: center; gap: 0.75rem; max-width: 550px;
    padding: 0.4rem 0.4rem 0.4rem 1.25rem;
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px; backdrop-filter: blur(25px);
}
.quick-cities {
    display: flex !important; flex-wrap: wrap; align-items: center;
    gap: 0.75rem; margin-top: 1rem;
}
.quick-city-btn {
    padding: 0.5rem 1.25rem; border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.8) !important; font-size: 0.85rem; text-decoration: none !important;
    cursor: pointer;
}
.quick-city-btn:hover { background: rgba(255,255,255,0.1); color: #fff !important; }

.hero-section {
    display: flex !important; flex-direction: row !important;
    justify-content: space-between !important; align-items: flex-end !important;
    margin-bottom: 3rem; padding-top: 2rem; width: 100%; gap: 2rem;
}
.location-info { flex: 1; min-width: 0; }
.location-header {
    display: flex !important; align-items: center; gap: 0.75rem;
}
.location-header h1 { font-family: var(--font-heading); font-size: 2.5rem; font-weight: 600; margin: 0; }
.date-time { color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 1.5rem; }
.current-temp-large { text-align: right; flex-shrink: 0; }
.temp-row {
    display: flex !important; align-items: center; justify-content: flex-end; gap: 1.5rem;
}
.condition-info {
    display: flex !important; align-items: center; justify-content: flex-end;
    gap: 0.5rem; font-size: 1.4rem; color: var(--text-secondary); margin-top: 0.25rem;
}
.temp-value { font-family: var(--font-heading); font-size: 6rem; font-weight: 700; line-height: 1; }
.condition-info { font-size: 1.5rem; color: var(--text-secondary); display: flex; align-items: center; justify-content: flex-end; gap: 0.5rem; }

.metrics-grid {
    display: grid !important; grid-template-columns: repeat(8, 1fr) !important;
    gap: 1rem; margin-bottom: 2rem; width: 100%;
}
.metric-card {
    background: rgba(255,255,255,0.05); backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1); padding: 1.25rem 1rem; border-radius: 16px;
    display: flex; flex-direction: column; align-items: center; gap: 0.75rem;
}
.metric-label { font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.metric-value { font-family: var(--font-heading); font-size: 1.15rem; font-weight: 700; }

.dashboard-layout {
    display: grid !important; grid-template-columns: 2fr 1fr !important;
    gap: 1.5rem; width: 100%; align-items: start;
}
.dashboard-main, .dashboard-sidebar {
    display: flex !important; flex-direction: column !important;
    gap: 1.5rem; width: 100%; min-width: 0;
}
.card {
    background: rgba(255,255,255,0.04); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1.5rem;
}
.card h2 { font-family: var(--font-heading); font-size: 1.1rem; font-weight: 600; margin: 0 0 1.5rem; display: flex; align-items: center; gap: 0.75rem; }
.trends-row {
    display: grid !important; grid-template-columns: 1fr 1fr !important;
    gap: 1.5rem; width: 100%;
}
.chart-card { min-height: 200px; }

.aqi-detailed { display: flex; flex-direction: column; gap: 1.5rem; }
.aqi-main { display: flex; align-items: center; gap: 1.5rem; }
.aqi-gauge-large {
    width: 80px; height: 80px; border-radius: 50%; border: 4px solid #4ade80;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 700; flex-shrink: 0;
}
.aqi-status-badge { padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 0.4rem; }
.aqi-status-desc { font-size: 0.8rem; color: rgba(255,255,255,0.6); line-height: 1.4; margin: 0; }
.pollutant-item { display: flex; flex-direction: column; gap: 0.4rem; }
.pollutant-info { display: flex; justify-content: space-between; font-size: 0.8rem; }
.pollutant-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.pollutant-fill { height: 100%; background: #4facfe; border-radius: 2px; }

.forecast-row {
    display: grid !important; grid-template-columns: 100px 1fr 80px !important; align-items: center;
    padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.forecast-row:last-child { border-bottom: none; }
.forecast-temps .min { color: rgba(255,255,255,0.4); margin-left: 0.5rem; }

.radar-card-main { padding: 0 !important; overflow: hidden; }
.radar-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: space-between; }
.radar-container { height: 350px; width: 100%; background: #1a1c22; border-radius: 0 0 20px 20px; }

.page-header { margin-bottom: 2rem; }
.page-header h1 { font-family: var(--font-heading); font-size: 2.5rem; margin: 0 0 0.5rem; }
.page-header p { color: var(--text-secondary); font-size: 1.1rem; margin: 0; }

.daily-detail-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem; }
.detail-forecast-card { display: flex; flex-direction: column; gap: 1.5rem; }
.detail-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border); padding-bottom: 1rem; }
.detail-body { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.temp-range { display: flex; gap: 1rem; font-size: 2rem; font-family: var(--font-heading); font-weight: 700; }
.temp-range .min { color: var(--text-secondary); }
.detail-footer { display: flex; justify-content: space-around; padding-top: 1rem; border-top: 1px solid var(--card-border); }
.footer-stat { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-secondary); }

.analysis-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
.analysis-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2rem; }
.stat-card { display: flex; flex-direction: column; gap: 0.5rem; align-items: center; padding: 2rem; text-align: center; }
.stat-label { color: var(--text-secondary); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; }
.stat-value { font-size: 2.5rem; font-weight: 700; font-family: var(--font-heading); }
.stat-change.up { color: var(--success-color); font-size: 0.85rem; font-weight: 600; }
.stat-change.down { color: var(--danger-text); font-size: 0.85rem; font-weight: 600; }

.map-app .page-content { padding: 0 !important; max-width: none !important; margin: 0 !important; }
.map-page-wrapper { position: relative; height: calc(100vh - 64px); min-height: 500px; overflow: hidden; background: #0a0c10; }
.map-stage { position: relative; width: 100%; height: 100%; }
.map-leaflet-fill,
.map-stage .nicegui-leaflet {
    position: absolute !important; inset: 0 !important;
    width: 100% !important; height: 100% !important; z-index: 1 !important;
}
.map-ui-layer {
    position: absolute; inset: 0; z-index: 500;
    pointer-events: none; overflow: visible;
}
.map-float { position: absolute; pointer-events: auto; }
.map-view-float { top: 16px; right: 16px; z-index: 600; }
.map-chrome-panels {
    position: absolute; inset: 0; pointer-events: none;
}
.map-chrome-panels > .map-float { pointer-events: auto; }
.map-chrome-panels--hidden {
    opacity: 0 !important; visibility: hidden !important; pointer-events: none !important;
}
.map-stage .leaflet-control-zoom { display: none !important; }
.map-sidebar-float { top: 80px; left: 16px; width: 200px; }
.map-location-float {
    top: 80px; right: 16px; width: 300px; max-width: calc(100vw - 32px);
    overflow: visible;
}
.map-location-float .map-location-card { max-width: 100%; }
.map-timeline-float {
    bottom: 20px; left: 50%; transform: translateX(-50%);
    width: min(640px, calc(100vw - 40px));
    z-index: 650;
    pointer-events: auto;
}
.map-legend-float { bottom: 20px; right: 16px; width: 300px; max-width: calc(100vw - 32px); }

.map-menu-card {
    background: rgba(18, 20, 28, 0.82); backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 0.35rem;
    display: flex; flex-direction: column; gap: 0.15rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}
.map-menu-item {
    display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 1rem;
    color: rgba(255,255,255,0.75); border-radius: 10px; cursor: pointer; font-size: 0.9rem;
    transition: background 0.2s ease, color 0.2s ease;
}
.map-menu-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.map-menu-item.active { background: #ff5722; color: #fff; font-weight: 600; }
.map-menu-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 0.35rem 0.5rem; }
.map-menu-footer {
    padding: 0.65rem 1rem; display: flex; align-items: center;
    justify-content: space-between; font-size: 0.82rem; color: rgba(255,255,255,0.55);
}

.map-location-card {
    background: rgba(18, 20, 28, 0.88); backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 1.1rem 1.25rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    overflow: hidden; position: relative; isolation: isolate;
    width: 100%; box-sizing: border-box;
}
.map-location-title { font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.2rem; }
.map-location-coords { font-size: 0.78rem; color: rgba(255,255,255,0.45); font-family: monospace; margin-bottom: 1rem; }
.map-location-main {
    display: flex !important; flex-direction: row !important; align-items: center !important;
    gap: 0.85rem; width: 100%; margin-bottom: 0.75rem; box-sizing: border-box;
}
.map-location-icon-wrap {
    flex: 0 0 56px; width: 56px; height: 56px; position: relative;
    display: flex !important; align-items: center !important; justify-content: center !important;
    border-radius: 14px; overflow: hidden;
    background: linear-gradient(145deg, rgba(255, 183, 77, 0.22), rgba(255, 152, 0, 0.08));
    border: 1px solid rgba(255, 183, 77, 0.25);
}
.map-location-icon-wrap > * {
    display: flex !important; align-items: center !important; justify-content: center !important;
    width: 100%; height: 100%; margin: 0 !important; padding: 0 !important;
}
.map-location-weather-glyph {
    font-size: 2.1rem !important; line-height: 1 !important;
}
.map-location-weather-glyph.icon-sunny {
    color: #ffca28 !important;
    text-shadow: 0 0 12px rgba(255, 202, 40, 0.35);
}
.map-location-weather-glyph.icon-night {
    color: #90caf9 !important;
    text-shadow: 0 0 10px rgba(144, 202, 249, 0.35);
}
.map-location-weather-glyph.icon-rain {
    color: #4fc3f7 !important;
    text-shadow: 0 0 10px rgba(79, 195, 247, 0.35);
}
.map-location-weather-glyph.icon-cloud {
    color: #b0bec5 !important;
}
.map-location-weather-glyph.icon-storm {
    color: #ce93d8 !important;
}
.map-location-weather-glyph.icon-snow {
    color: #e3f2fd !important;
}
.map-location-weather-glyph.icon-fog {
    color: #cfd8dc !important;
}
.map-location-metric-wrap {
    display: flex !important; flex-direction: row !important; align-items: baseline !important;
    gap: 0.35rem; flex: 1 1 auto; min-width: 0;
}
.map-location-main-value {
    font-size: 2.35rem; font-weight: 700; font-family: var(--font-heading);
    line-height: 1; color: #fff; white-space: nowrap;
}
.map-location-main-unit {
    font-size: 1.05rem; color: rgba(255,255,255,0.55); white-space: nowrap;
}
.map-location-details { display: flex; flex-direction: column; gap: 0.45rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.08); }
.map-location-row-label { font-size: 0.82rem; color: rgba(255,255,255,0.5); }
.map-location-row-value { font-size: 0.82rem; color: rgba(255,255,255,0.9); font-weight: 500; }


/* Glassmorphism round icon button for map floating actions */
.round-icon-btn {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    min-width: unset !important;
    padding: 0 !important;
    transition: all 0.35s ease;
}
.round-icon-btn .q-btn__content {
    background: transparent !important;
}
.round-icon-btn::before,
.round-icon-btn::after {
    display: none !important;
}

/* Base map nhạt — lớp thời tiết nổi bật */
.map-leaflet .leaflet-tile-pane:first-child .leaflet-tile {
    filter: brightness(1.08) saturate(0.78) contrast(0.92);
}
.map-leaflet .leaflet-overlay-pane .leaflet-tile {
    filter: none;
    transition: opacity 0.2s ease;
}
.map-timeline-slider .q-slider__track-container--h { height: 5px; }
.map-timeline-slider .q-slider__thumb { width: 16px; height: 16px; }
.timeline-card {
    background: rgba(18, 20, 28, 0.88); backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 0.75rem 1rem;
    display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
    align-items: center; gap: 0.65rem; width: 100%;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}
.timeline-nav-btn { color: rgba(255,255,255,0.7) !important; min-width: 36px !important; }
.timeline-time-label {
    font-size: 0.8rem; color: rgba(255,255,255,0.75); font-family: monospace;
    white-space: nowrap; min-width: 130px; text-align: right;
}
.legend-card {
    background: rgba(18, 20, 28, 0.88); backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 0.85rem 1rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}
.legend-gradient {
    height: 10px; width: 100%; border-radius: 6px;
    transition: background 0.25s ease; margin-bottom: 0.5rem;
}
.legend-labels { display: flex; justify-content: space-between; }
.legend-end-label { font-size: 0.72rem; color: rgba(255,255,255,0.45); font-family: monospace; }

@media (max-width: 900px) {
    .map-location-float { width: 260px; top: 72px; right: 8px; }
    .map-legend-float { width: 260px; bottom: 88px; right: 8px; }
    .map-timeline-float { width: calc(100vw - 32px); bottom: 12px; }
    .map-sidebar-float { width: 180px; }
}

.app-footer {
    position: relative; margin-top: 6rem; padding: 4rem 2rem 3rem;
    background: rgba(0,0,0,0.85); backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255,255,255,0.1); z-index: 1;
}
.footer-container {
    max-width: 1200px; margin: 0 auto;
    display: grid !important; grid-template-columns: 1.5fr 1fr 1fr 1fr !important; gap: 3rem;
}
.footer-logo {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #4facfe 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.footer-column h4 { font-size: 1rem; font-weight: 700; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px; }
.footer-list { list-style: none; padding: 0; margin: 0; }
.footer-list a { color: rgba(255,255,255,0.6) !important; text-decoration: none !important; font-size: 0.95rem; }
.footer-bottom { max-width: 1200px; margin: 3rem auto 0; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); }
.footer-copy { font-size: 0.95rem; color: rgba(255,255,255,0.4); }

.profile-avatar {
    width: 38px; height: 38px; border-radius: 50%; background: #e91e63;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 0.85rem; cursor: pointer; color: #fff;
}
.icon-btn-round {
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.7); min-width: 38px !important; padding: 0 !important;
}

.q-input-dark .q-field__control { background: transparent !important; color: #fff !important; }
.q-input-dark input { color: #fff !important; }
.q-btn-search { background: #00f2fe !important; color: #0a0c10 !important; font-weight: 700 !important; border-radius: 999px !important; }

@media (max-width: 1024px) {
    .dashboard-layout { grid-template-columns: 1fr; }
    .metrics-grid { grid-template-columns: repeat(4, 1fr); }
    .analysis-row { grid-template-columns: 1fr; }
    .footer-container { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 768px) {
    .nav-links { display: none; }
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .trends-row { grid-template-columns: 1fr; }
    .hero-section { flex-direction: column; align-items: flex-start; }
    .current-temp-large { text-align: left; }
    .temp-row, .condition-info { justify-content: flex-start; }
    .temp-value { font-size: 4rem; }
    .analysis-metrics { grid-template-columns: 1fr; }
}
"""
