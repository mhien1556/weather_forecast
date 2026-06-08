"""Giao diện glassmorphism — CSS nhúng qua Python (NiceGUI).
Hỗ trợ chuyển đổi Dark/Light mode hoàn toàn qua Quasar class .body--dark / .body--light.
NiceGUI tự động thêm class này khi gọi ui.dark_mode(True/False) — không cần JavaScript.
"""

STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════════════════════════════════════════
   DARK MODE — Quasar tự thêm class .body--dark khi ui.dark_mode(True)
   ══════════════════════════════════════════════════════════════════════════════ */
:root {
    --accent-color: #4facfe;
    --font-main: 'Inter', sans-serif;
    --font-heading: 'Outfit', sans-serif;
}

.body--dark {
    --primary-bg: #0a0c10;
    --card-bg: rgba(26, 32, 44, 0.95);
    --card-bg-solid: #1a202c;
    --card-border: rgba(255, 255, 255, 0.1);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.6);
    --text-muted: rgba(255, 255, 255, 0.4);
    --danger-text: #f87171;
    --success-color: #4ade80;

    --navbar-bg: rgba(11, 12, 16, 0.95);
    --navbar-text: #ffffff;
    --navbar-text-secondary: rgba(255, 255, 255, 0.6);
    --navbar-border: rgba(255, 255, 255, 0.12);
    --navbar-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    --navbar-link-hover: #4facfe;

    --logo-color-start: #ffffff;
    --logo-color-end: #4facfe;

    --search-bg: rgba(255, 255, 255, 0.1);
    --search-border: rgba(255, 255, 255, 0.25);
    --search-text: #ffffff;

    --footer-bg: rgba(0, 0, 0, 0.85);
    --footer-text: rgba(255, 255, 255, 0.7);
    --footer-text-muted: rgba(255, 255, 255, 0.5);
    --footer-border: rgba(255, 255, 255, 0.1);
    --footer-link: rgba(255, 255, 255, 0.6);
    --footer-heading: #ffffff;

    --menu-bg: rgba(18, 20, 28, 0.97);
    --menu-border: rgba(255, 255, 255, 0.1);
    --menu-text: rgba(255, 255, 255, 0.8);
    --menu-text-name: #ffffff;
    --menu-text-email: rgba(255, 255, 255, 0.45);
    --menu-hover: rgba(255, 255, 255, 0.07);
    --menu-separator: rgba(255, 255, 255, 0.08);

    --icon-btn-bg: rgba(255, 255, 255, 0.05);
    --icon-btn-border: rgba(255, 255, 255, 0.1);
    --icon-btn-color: rgba(255, 255, 255, 0.7);

    --input-bg: transparent;
    --input-text: #ffffff;

    --metric-label: rgba(255, 255, 255, 0.5);

    --hero-overlay-start: rgba(10, 12, 16, 0.2);
    --hero-overlay-end: rgba(10, 12, 16, 0.92);

    --separator-color: rgba(255, 255, 255, 0.08);
    --hover-bg: rgba(255, 255, 255, 0.1);

    --login-btn-bg: rgba(255, 255, 255, 0.07);
    --login-btn-border: rgba(255, 255, 255, 0.2);
    --login-btn-text: #ffffff;

    --glass-card-bg: rgba(255, 255, 255, 0.10);
    --glass-card-border: rgba(255, 255, 255, 0.18);
}

/* ══════════════════════════════════════════════════════════════════════════════
   LIGHT MODE — Quasar tự thêm class .body--light khi ui.dark_mode(False)
   ══════════════════════════════════════════════════════════════════════════════ */
.body--light {
    --primary-bg: #f4f6f9;
    --card-bg: #f5f5f5;  /* Softer light gray for comfortable eyes */
    --card-bg-solid: #ffffff;
    --card-border: rgba(0, 0, 0, 0.08);
    --text-primary: #1a1a2e;
    --text-secondary: rgba(0, 0, 0, 0.75); /* Tăng độ tương phản */
    --text-muted: rgba(0, 0, 0, 0.6);    /* Tăng độ tương phản */
    --danger-text: #dc2626;
    --success-color: #16a34a;

    --navbar-bg: rgba(255, 255, 255, 0.95);
    --navbar-text: #1a1a2e;
    --navbar-text-secondary: rgba(0, 0, 0, 0.7); /* Tăng độ tương phản cho Light Mode */
    --navbar-border: rgba(0, 0, 0, 0.08);
    --navbar-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    --navbar-link-hover: #4facfe;

    --logo-color-start: #1a1a2e;
    --logo-color-end: #4facfe;

    --search-bg: rgba(0, 0, 0, 0.05);
    --search-border: rgba(0, 0, 0, 0.12);
    --search-text: #1a1a2e;

    --footer-bg: rgba(245, 247, 250, 0.98);
    --footer-text: rgba(0, 0, 0, 0.75); /* Tăng độ tương phản */
    --footer-text-muted: rgba(0, 0, 0, 0.6);    /* Tăng độ tương phản */
    --footer-border: rgba(0, 0, 0, 0.08);
    --footer-link: rgba(0, 0, 0, 0.7); /* Tăng độ tương phản cho Light Mode */
    --footer-heading: #1a1a2e;

    --menu-bg: rgba(255, 255, 255, 0.98);
    --menu-border: rgba(0, 0, 0, 0.08);
    --menu-text: rgba(0, 0, 0, 0.7);
    --menu-text-name: #1a1a2e;
    --menu-text-email: rgba(0, 0, 0, 0.45);
    --menu-hover: rgba(0, 0, 0, 0.05);
    --menu-separator: rgba(0, 0, 0, 0.08);

    --icon-btn-bg: rgba(0, 0, 0, 0.05);
    --icon-btn-border: rgba(0, 0, 0, 0.1);
    --icon-btn-color: rgba(0, 0, 0, 0.55);

    --input-bg: rgba(0, 0, 0, 0.03);
    --input-text: #1a1a2e;

    --metric-label: rgba(0, 0, 0, 0.65); /* Tăng độ tương phản */

    --hero-overlay-start: rgba(244, 246, 249, 0.1);
    --hero-overlay-end: rgba(244, 246, 249, 0.95);

    --separator-color: rgba(0, 0, 0, 0.08);
    --hover-bg: rgba(0, 0, 0, 0.05);

    --login-btn-bg: rgba(0, 0, 0, 0.05);
    --login-btn-border: rgba(0, 0, 0, 0.15);
    --login-btn-text: #1a1a2e;

    --glass-card-bg: rgba(255, 255, 255, 0.70);
    --glass-card-border: rgba(0, 0, 0, 0.10);
}

/* ══════════════════════════════════════════════════════════════════════════════
   LIGHT MODE — Quasar component overrides (Quasar tự thêm màu riêng, cần force)
   ══════════════════════════════════════════════════════════════════════════════ */
.body--light .q-field__native,
.body--light .q-field__label,
.body--light .q-field__marginal,
.body--light .q-item,
.body--light .q-item__label,
.body--light .q-item__section,
.body--light .q-radio__label,
.body--light .q-checkbox__label,
.body--light .q-toggle__label,
.body--light .q-option-group,
.body--light label,
.body--light .q-label,
.body--light .q-card,
.body--light .q-card * {
    color: var(--text-primary) !important;
}
.body--light .q-separator {
    background: rgba(0, 0, 0, 0.10) !important;
}
.body--light .q-btn.q-btn--flat .q-icon,
.body--light .icon-btn-round .q-icon {
    color: var(--icon-btn-color) !important;
}
/* Quasar switch/toggle track trên light mode */
.body--light .q-toggle__track { opacity: 0.5; }
/* Navbar icon buttons trên light mode không bị trắng chữ */
.body--light .navbar .q-icon { color: var(--icon-btn-color) !important; }
/* Input text trong search bar */
.body--light .city-search-bar input,
.body--light .q-input .q-field__native {
    color: var(--search-text) !important;
}
/* Đảm bảo text trong hero section đọc được trên light */
.body--light .temp-value,
.body--light .location-header h1,
.body--light .date-time,
.body--light .condition-info {
    text-shadow: 0 1px 8px rgba(0,0,0,0.18);
}

/* ══════════════════════════════════════════════════════════════════════════════
   GLOBAL — áp dụng cả dark và light
   ══════════════════════════════════════════════════════════════════════════════ */

html, body, .nicegui-content, .q-layout, .q-page, .q-page-container, #app {
    font-family: var(--font-main) !important;
    background-color: var(--primary-bg) !important;
    background: var(--primary-bg) !important;
    color: var(--text-primary) !important;
    margin: 0;
    margin: 0 !important; padding: 0 !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.q-card, .q-dialog__inner > .q-card {
    background: var(--card-bg) !important;
    color: var(--text-primary) !important;
}

/* ── Quasar text elements — buộc dùng CSS variable, không để Quasar tự set ── */
.q-field__native, .q-field__label, .q-field__marginal,
.q-item, .q-item__label, .q-item__section,
.q-radio__label, .q-checkbox__label,
.q-toggle__label, .q-option-group,
.q-select__dropdown-icon,
label, .q-label {
    color: var(--text-primary) !important;
}

/* Input placeholder */
.q-field__native::placeholder,
input::placeholder {
    color: var(--text-secondary) !important;
    opacity: 1 !important;
}

/* Chỉ override màu chữ button flat/outline, không override unelevated/filled */
.q-btn.q-btn--flat, .q-btn.q-btn--outline {
    color: var(--text-primary) !important;
}

/* Icon trong các button flat thường (settings, search...) */
.icon-btn-round .q-icon,
.q-btn.q-btn--flat .q-icon {
    color: var(--icon-btn-color) !important;
}

/* Separator */
.q-separator { background: var(--separator-color) !important; }

/* Menu/popup items */
.q-menu { background: var(--menu-bg) !important; border: 1px solid var(--menu-border) !important; }
.q-item:hover { background: var(--menu-hover) !important; }

/* Switch thumb color */
.q-toggle__inner--truthy { color: var(--accent-color) !important; }

a, .q-link { color: inherit !important; }

.app-container {
    position: relative; min-height: 100vh; width: 100%;
    background-color: var(--primary-bg) !important;
    transition: background-color 0.3s ease;
}

.hero-bg {
    position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
    z-index: 0; pointer-events: none;
    background: var(--primary-bg);
    overflow: hidden;
}
.hero-bg .overlay {
    position: absolute; inset: 0;
    background: 
        radial-gradient(circle at 20% 20%, var(--accent-color), transparent 40%),
        radial-gradient(circle at 80% 80%, var(--accent-color), transparent 40%),
        linear-gradient(to bottom, var(--hero-overlay-start) 0%, var(--hero-overlay-end) 100%);
    opacity: 0.4;
    transition: background 0.5s ease;
}

div { box-sizing: border-box; }
.page-content { position: relative; z-index: 1; padding-left: 1cm; padding-right: 1cm; }

/* ══════════════════════════════════════════════════════════════════════════════
   NAVBAR — chuyển màu hoàn toàn theo dark/light class
   ══════════════════════════════════════════════════════════════════════════════ */
.navbar {
    display: flex !important; justify-content: space-between; align-items: center;
    padding: 0.75rem 1.5rem; /* horizontal padding for inner content */
    background: var(--navbar-bg) !important;
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--navbar-border) !important;
    position: sticky; top: 0; z-index: 1000;
    box-shadow: var(--navbar-shadow) !important;
    transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    width: 100% !important; max-width: 100% !important;
}
.q-header, nav { left: 0 !important; right: 0 !important; width: 100% !important; }

.logo-gradient {
    font-weight: 800; font-size: 1.6rem; letter-spacing: -0.5px;
    background: linear-gradient(90deg, var(--logo-color-start) 0%, var(--logo-color-end) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    cursor: pointer; text-decoration: none !important;
    transition: background 0.3s ease;
}

.nav-links {
    display: flex !important; flex-direction: row !important; flex-wrap: wrap;
    gap: 2rem !important; list-style: none; margin: 0; padding: 0; align-items: center;
}
.nav-left  { display: flex !important; align-items: center; gap: 3rem; }
.nav-right { display: flex !important; align-items: center; gap: 1.25rem; }
.nav-search {
    flex: 1; max-width: 450px; margin: 0 2rem;
    display: flex !important; align-items: center; gap: 0.5rem;
}

.nav-link {
    font-size: 1.05rem !important; font-weight: 600 !important;
    transition: all 0.2s ease; cursor: pointer; padding: 6px 12px !important;
    border-bottom: none !important;
    color: var(--navbar-text-secondary) !important;
    opacity: 1;
}
.nav-link:hover { color: var(--navbar-link-hover) !important; }
.nav-link.active {
    color: var(--navbar-link-hover) !important;
    font-weight: 700 !important;
}
.nav-links a, .nav-links .nav-link {
    text-decoration: none !important;
    color: var(--navbar-text-secondary) !important;
    font-weight: 600; font-size: 0.95rem; padding: 0.5rem 0; position: relative;
    cursor: pointer; transition: color 0.2s ease;
}
.nav-links a:hover, .nav-links a.active,
.nav-links .nav-link:hover, .nav-links .nav-link.active {
    color: var(--navbar-link-hover) !important;
}
.nav-links a.active::after, .nav-links .nav-link.active::after {
    content: ''; position: absolute; bottom: -2px; left: 0;
    width: 100%; height: 3px; background: var(--accent-color); border-radius: 4px;
}

/* ── Search bar trong navbar ── */
.city-search-bar {
    background: var(--search-bg) !important;
    border: 1px solid var(--search-border) !important;
    border-radius: 99px !important; padding: 4px 6px 4px 18px !important;
    display: flex; align-items: center; transition: all 0.3s ease;
    max-width: 100%; margin: 0; width: 260px;
}
.city-search-bar:focus-within {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 15px rgba(79, 172, 254, 0.3);
}

/* ── Login button ── */
.q-btn-login {
    background: var(--login-btn-bg) !important;
    border: 1px solid var(--login-btn-border) !important;
    color: var(--login-btn-text) !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s ease;
}
.q-btn-login:hover { background: var(--hover-bg) !important; }

/* ── Icon buttons ── */
.icon-btn-round {
    width: 38px; height: 38px; border-radius: 50%;
    background: var(--icon-btn-bg) !important;
    border: 1px solid var(--icon-btn-border) !important;
    color: var(--icon-btn-color) !important;
    min-width: 38px !important; padding: 0 !important;
    transition: background 0.3s ease, border-color 0.3s ease;
}

/* ── User menu dropdown ── */
.user-menu-wrapper { position: relative; }
.user-dropdown-menu {
    background: var(--menu-bg) !important;
    border: 1px solid var(--menu-border) !important;
    border-radius: 16px !important; padding: 0.5rem !important;
    min-width: 230px !important; box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
    transition: background 0.3s ease, border-color 0.3s ease;
}
.user-menu-header {
    display: flex !important; align-items: center; gap: 0.75rem;
    padding: 0.5rem 0.75rem 0.75rem;
}
.user-menu-avatar {
    width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg, #e91e63, #9c27b0);
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 1rem; flex-shrink: 0;
}
.user-menu-item {
    border-radius: 10px !important;
    color: var(--menu-text) !important;
    font-size: 0.9rem !important;
    transition: background 0.2s ease;
}
.user-menu-item:hover { background: var(--menu-hover) !important; color: var(--text-primary) !important; }
.user-menu-logout { color: #f87171 !important; }
.user-menu-logout:hover { background: rgba(239,68,68,0.1) !important; }

/* ── Profile avatar ── */
.profile-avatar {
    width: 38px; height: 38px; border-radius: 50%; background: #e91e63;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 0.85rem; cursor: pointer; color: #fff;
}

/* ══════════════════════════════════════════════════════════════════════════════
   FOOTER — chuyển màu hoàn toàn theo dark/light class
   ══════════════════════════════════════════════════════════════════════════════ */
.app-footer {
    position: relative; margin-top: 6rem; padding: 4rem 1.5rem 3rem; /* vertical padding with horizontal inset */
    background: var(--footer-bg) !important; backdrop-filter: blur(20px);
    border-top: 1px solid var(--footer-border) !important; z-index: 1;
    transition: background 0.3s ease, border-color 0.3s ease;
    width: 100% !important; max-width: 100% !important;
}
.footer-container {
    width: 100%; margin: 0; /* full‑width, no centering */
    display: grid !important; grid-template-columns: 1.5fr 1fr 1fr 1fr !important; gap: 3rem;
}
.footer-logo {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--footer-heading) 0%, var(--accent-color) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.footer-column h4 {
    font-size: 1rem; font-weight: 700; margin-bottom: 1.5rem;
    text-transform: uppercase; letter-spacing: 1px;
    color: var(--footer-heading) !important;
}
.footer-list { list-style: none; padding: 0; margin: 0; }
.footer-list a {
    color: var(--footer-link) !important; text-decoration: none !important; font-size: 0.95rem;
    transition: color 0.2s ease;
}
.footer-list a:hover { color: var(--accent-color) !important; }
.footer-bottom {
    max-width: 1200px; margin: 3rem auto 0; padding-top: 2rem;
    border-top: 1px solid var(--footer-border);
}
.footer-copy { font-size: 0.95rem; color: var(--footer-text-muted); }

/* ══════════════════════════════════════════════════════════════════════════════
   CONTENT LAYOUT
   ══════════════════════════════════════════════════════════════════════════════ */
.content-wrapper {
    max-width: 100%; margin: 0; padding: 2rem 1.5rem;
    width: 100%; box-sizing: border-box;
}
.city-search-bar-wrap { margin-bottom: 1.5rem; padding-top: 0.5rem; }
.quick-cities {
    display: flex !important; flex-wrap: wrap; align-items: center;
    gap: 0.75rem; margin-top: 1rem;
}
.quick-city-btn {
    padding: 0.5rem 1.25rem; border-radius: 999px;
    border: 1px solid var(--card-border); background: var(--card-bg);
    color: var(--text-secondary) !important; font-size: 0.85rem; text-decoration: none !important;
    cursor: pointer; transition: all 0.2s ease;
}
.quick-city-btn:hover { background: var(--hover-bg); color: var(--text-primary) !important; }

/* ── Hero Section ── */
.hero-section {
    display: flex !important; flex-direction: row !important;
    justify-content: space-between !important; align-items: flex-end !important;
    margin-bottom: 3rem; padding-top: 2rem; width: 100%; gap: 2rem;
}
.location-info { flex: 1; min-width: 0; }
.location-header { display: flex !important; align-items: center; gap: 0.75rem; }
.location-header h1 { font-family: var(--font-heading); font-size: 2.5rem; font-weight: 600; margin: 0; }
.date-time { color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 1.5rem; }
.current-temp-large { text-align: right; flex-shrink: 0; }
.temp-row { display: flex !important; align-items: center; justify-content: flex-end; gap: 1.5rem; }
.condition-info {
    display: flex !important; align-items: center; justify-content: flex-end;
    gap: 0.5rem; font-size: 1.5rem; color: var(--text-secondary); margin-top: 0.25rem;
}
.temp-value {
    font-family: var(--font-heading); font-size: 6rem; font-weight: 700; line-height: 1;
    color: var(--text-primary);
}

/* ── Metrics ── */
.metrics-grid {
    display: grid !important; grid-template-columns: repeat(8, 1fr) !important;
    gap: 1rem; margin-bottom: 2rem; width: 100%;
}
.metric-card {
    background: var(--glass-card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid var(--glass-card-border);
    padding: 1.25rem 1rem;
    display: flex; flex-direction: column; align-items: center; gap: 0.75rem;
    color: var(--text-primary);
    transition: background 0.3s ease, border-color 0.2s ease;
}
.metric-label {
    font-size: 0.75rem; color: var(--metric-label); text-transform: uppercase;
    letter-spacing: 0.5px; font-weight: 600;
}
.metric-value { font-family: var(--font-heading); font-size: 1.15rem; font-weight: 700; color: var(--text-primary); }

/* ── Cards ── */
.card {
    background: var(--glass-card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid var(--glass-card-border);
}
.card h2 { font-family: var(--font-heading); font-size: 1.1rem; font-weight: 600; margin: 0 0 1.5rem; display: flex; align-items: center; gap: 0.75rem; }

/* ── Dashboard ── */
.dashboard-layout {
    display: grid !important; grid-template-columns: 2fr 1fr !important;
    gap: 1.5rem; width: 100%; align-items: start;
}
.dashboard-main, .dashboard-sidebar {
    display: flex !important; flex-direction: column !important;
    gap: 1.5rem; width: 100%; min-width: 0;
}
.trends-row { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 1.5rem; width: 100%; }
.chart-card { min-height: 200px; }

/* ── AQI ── */
.aqi-detailed { display: flex; flex-direction: column; gap: 1.5rem; }
.aqi-main { display: flex; align-items: center; gap: 1.5rem; }
.aqi-gauge-large {
    width: 80px; height: 80px; border-radius: 50%; border: 4px solid #4ade80;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 700; flex-shrink: 0;
}
.aqi-status-badge { padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 0.4rem; }
.aqi-status-desc { font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin: 0; }
.pollutant-item { display: flex; flex-direction: column; gap: 0.4rem; }
.pollutant-info { display: flex; justify-content: space-between; font-size: 0.8rem; }
.pollutant-bar { height: 4px; background: var(--card-border); border-radius: 2px; overflow: hidden; }
.pollutant-fill { height: 100%; background: #4facfe; border-radius: 2px; }

/* ── Forecast ── */
.forecast-row {
    display: grid !important; grid-template-columns: 100px 1fr 80px !important;
    align-items: center; padding: 0.75rem 0;
    border-bottom: 1px solid var(--separator-color);
}
.forecast-row:last-child { border-bottom: none; }
.forecast-temps .min { color: var(--text-muted); margin-left: 0.5rem; }

/* ── Radar ── */
.radar-card-main { padding: 0 !important; overflow: hidden; }
.radar-header {
    padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--separator-color);
    display: flex; align-items: center; justify-content: space-between;
}
.radar-container { height: 350px; width: 100%; background: var(--card-bg-solid); border-radius: 0 0 20px 20px; }

/* ── Page Header ── */
.page-header { margin-bottom: 2rem; }
.page-header h1 { font-family: var(--font-heading); font-size: 2.5rem; margin: 0 0 0.5rem; color: var(--text-primary); }
.page-header p { color: var(--text-secondary); font-size: 1.1rem; margin: 0; }

/* ── Forecast Detail Cards ── */
.daily-detail-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem; }
.detail-forecast-card {
    background: var(--glass-card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid var(--glass-card-border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    color: var(--text-primary);
    transition: background 0.3s ease, border-color 0.2s ease;
}
.detail-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border); padding-bottom: 1rem; }
.detail-body { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.temp-range { display: flex; gap: 1rem; font-size: 2rem; font-family: var(--font-heading); font-weight: 700; }
.temp-range .min { color: var(--text-secondary); }
.detail-footer { display: flex; justify-content: space-around; padding-top: 1rem; border-top: 1px solid var(--card-border); }
.footer-stat { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-secondary); }

/* ── Analysis ── */
.analysis-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
.analysis-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2rem; }
.stat-card { display: flex; flex-direction: column; gap: 0.5rem; align-items: center; padding: 2rem; text-align: center; }
.stat-label { color: var(--text-secondary); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; }
.stat-value { font-size: 2.5rem; font-weight: 700; font-family: var(--font-heading); color: var(--text-primary); }
.stat-change.up { color: var(--success-color); font-size: 0.85rem; font-weight: 600; }
.stat-change.down { color: var(--danger-text); font-size: 0.85rem; font-weight: 600; }

.analysis-kpi-row {
    display: grid !important; grid-template-columns: repeat(4, 1fr) !important;
    gap: 1rem; margin-bottom: 1.5rem;
}
.kpi-card {
    display: flex !important; flex-direction: column !important; gap: 0.5rem;
    transition: transform 0.3s, background 0.3s;
}
.kpi-card:hover { transform: translateY(-4px); background: var(--hover-bg) !important; }
.analysis-bottom {
    display: grid !important; grid-template-columns: 1fr 2fr !important;
    gap: 1.5rem; margin-bottom: 2rem; align-items: start;
}

/* ── Settings ── */
.q-dialog__inner > .settings-dialog-card, .settings-dialog-card {
    width: min(860px, calc(100vw - 32px));
    max-height: min(760px, calc(100vh - 32px));
    overflow-y: auto; border-radius: 18px !important;
    border: 1px solid var(--card-border);
    background: var(--card-bg-solid) !important;
    box-shadow: 0 24px 70px rgba(0,0,0,0.55);
}
.settings-section-card { border-radius: 12px !important; padding: 1.1rem !important; }
.settings-option-row { display: flex !important; align-items: center; gap: 1rem; flex-wrap: wrap; width: 100%; }
.settings-option-label { min-width: 130px; font-weight: 600; color: var(--text-secondary); }

/* ── Inputs ── */
.q-input-dark .q-field__control { background: var(--input-bg) !important; color: var(--input-text) !important; }
.q-input-dark input { color: var(--input-text) !important; }
.q-btn-search { background: #00f2fe !important; color: #0a0c10 !important; font-weight: 700 !important; border-radius: 999px !important; }

/* ── Auth tabs ── */
.auth-tab { border-radius: 8px !important; color: var(--text-muted) !important; font-weight: 600 !important; transition: all 0.2s !important; }
.auth-tab-active { background: var(--hover-bg) !important; color: var(--text-primary) !important; }

/* ══════════════════════════════════════════════════════════════════════════════
   MAP STYLES — luôn dùng dark palette (map không đổi theo theme)
   ══════════════════════════════════════════════════════════════════════════════ */
.map-app .page-content { padding: 0 1cm !important; max-width: none !important; margin: 0 !important; }
.map-page-wrapper { position: relative; height: calc(100vh - 64px); min-height: 500px; overflow: hidden; background: #0a0c10; }
.map-stage { position: relative; width: 100%; height: 100%; }
.map-wind-particles { position: absolute; inset: 0; z-index: 480; pointer-events: none; width: 100%; height: 100%; }
.map-stage[class*="map-layer-"] .leaflet-tile-pane img.leaflet-tile { opacity: 1 !important; }
.legend-title { font-size: 0.82rem; font-weight: 700; color: rgba(255,255,255,0.97); margin-bottom: 0.45rem; letter-spacing: 0.02em; text-shadow: 0 1px 4px rgba(0,0,0,0.4); }
.legend-gradient { height: 12px; width: 100%; border-radius: 6px; transition: background 0.25s ease; margin-bottom: 0.5rem; }
.map-leaflet-fill, .map-stage .nicegui-leaflet { position: absolute !important; inset: 0 !important; width: 100% !important; height: 100% !important; z-index: 1 !important; }
.map-ui-layer { position: absolute; inset: 0; z-index: 500; pointer-events: none; overflow: visible; }
.map-float { position: absolute; pointer-events: auto; }
.map-view-float { top: 16px; right: 16px; z-index: 600; }
.map-chrome-panels { position: absolute; inset: 0; pointer-events: none; }
.map-chrome-panels > .map-float { pointer-events: auto; }
.map-chrome-panels--hidden { opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; }
.map-stage .leaflet-control-zoom { display: none !important; }
.map-sidebar-float { top: 80px; left: 16px; width: 200px; }
.map-location-float { top: 80px; right: 16px; width: 300px; max-width: calc(100vw - 32px); overflow: visible; }
.map-location-float .map-location-card { max-width: 100%; }
.map-timeline-float { bottom: 20px; left: 50%; transform: translateX(-50%); width: min(640px, calc(100vw - 40px)); z-index: 650; pointer-events: auto; }
.map-legend-float { bottom: 20px; right: 16px; width: 300px; max-width: calc(100vw - 32px); }

.map-menu-card { background: rgba(20,34,60,0.58); backdrop-filter: blur(20px) saturate(1.5); border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.35rem; display: flex; flex-direction: column; gap: 0.15rem; box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08); }
.map-menu-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 1rem; color: rgba(255,255,255,0.75); border-radius: 10px; cursor: pointer; font-size: 0.9rem; transition: background 0.2s ease, color 0.2s ease; }
.map-menu-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.map-menu-item.active { background: #ff5722; color: #fff; font-weight: 600; }
.map-menu-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 0.35rem 0.5rem; }
.map-menu-footer { padding: 0.65rem 1rem; display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; color: rgba(255,255,255,0.55); }

.map-location-card { background: rgba(20,34,60,0.58); backdrop-filter: blur(20px) saturate(1.5); border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 1.1rem 1.25rem; box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08); overflow: hidden; position: relative; isolation: isolate; width: 100%; box-sizing: border-box; }
.map-location-title { font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.2rem; }
.map-location-coords { font-size: 0.78rem; color: rgba(255,255,255,0.45); font-family: monospace; margin-bottom: 1rem; }
.map-location-main { display: flex !important; flex-direction: row !important; align-items: center !important; gap: 0.85rem; width: 100%; margin-bottom: 0.75rem; box-sizing: border-box; }
.map-location-icon-wrap { flex: 0 0 56px; width: 56px; height: 56px; position: relative; display: flex !important; align-items: center !important; justify-content: center !important; border-radius: 14px; overflow: hidden; background: linear-gradient(145deg, rgba(255,183,77,0.22), rgba(255,152,0,0.08)); border: 1px solid rgba(255,183,77,0.25); }
.map-location-icon-wrap > * { display: flex !important; align-items: center !important; justify-content: center !important; width: 100%; height: 100%; margin: 0 !important; padding: 0 !important; }
.map-location-weather-glyph { font-size: 2.1rem !important; line-height: 1 !important; }
.map-location-weather-glyph.icon-sunny { color: #ffca28 !important; text-shadow: 0 0 12px rgba(255,202,40,0.35); }
.map-location-weather-glyph.icon-night { color: #90caf9 !important; }
.map-location-weather-glyph.icon-rain { color: #4fc3f7 !important; }
.map-location-weather-glyph.icon-cloud { color: #b0bec5 !important; }
.map-location-weather-glyph.icon-storm { color: #ce93d8 !important; }
.map-location-weather-glyph.icon-snow { color: #e3f2fd !important; }
.map-location-weather-glyph.icon-fog { color: #cfd8dc !important; }
.map-location-metric-wrap { display: flex !important; flex-direction: row !important; align-items: baseline !important; gap: 0.35rem; flex: 1 1 auto; min-width: 0; }
.map-location-main-value { font-size: 2.35rem; font-weight: 700; font-family: var(--font-heading); line-height: 1; color: #fff; white-space: nowrap; }
.map-location-main-unit { font-size: 1.05rem; color: rgba(255,255,255,0.55); white-space: nowrap; }
.map-location-details { display: flex; flex-direction: column; gap: 0.45rem; padding-top: 0.75rem; border-top: 1px solid rgba(148,187,255,0.18); }
.map-location-row-label { font-size: 0.82rem; color: rgba(200,220,255,0.65); }
.map-location-row-value { font-size: 0.82rem; color: rgba(255,255,255,0.97); font-weight: 600; }

.round-icon-btn { width: 52px; height: 52px; border-radius: 16px; background: rgba(20,34,60,0.65); backdrop-filter: blur(20px) saturate(1.5); border: 1px solid rgba(148,187,255,0.22); color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08); min-width: unset !important; padding: 0 !important; transition: all 0.35s ease; }
.round-icon-btn .q-btn__content { background: transparent !important; }
.round-icon-btn::before, .round-icon-btn::after { display: none !important; }

.map-leaflet .leaflet-tile-pane:first-child .leaflet-tile { filter: brightness(1.08) saturate(0.78) contrast(0.92); }
.map-leaflet .leaflet-overlay-pane .leaflet-tile { filter: none; transition: opacity 0.2s ease; }
.map-timeline-slider .q-slider__track-container--h { height: 5px; }
.map-timeline-slider .q-slider__thumb { width: 16px; height: 16px; }
.timeline-card { background: rgba(20,34,60,0.58); backdrop-filter: blur(20px) saturate(1.5); border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.75rem 1rem; display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; align-items: center; gap: 0.65rem; width: 100%; box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08); }
.timeline-nav-btn { color: rgba(255,255,255,0.85) !important; min-width: 36px !important; }
.timeline-time-label { font-size: 0.8rem; color: rgba(255,255,255,0.9); font-family: monospace; white-space: nowrap; min-width: 130px; text-align: right; font-weight: 500; }
.legend-card { background: rgba(20,34,60,0.58); backdrop-filter: blur(20px) saturate(1.5); border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.85rem 1rem; box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08); }
.legend-labels { display: flex; justify-content: space-between; }
.legend-end-label { font-size: 0.72rem; color: rgba(255,255,255,0.7); font-family: monospace; font-weight: 500; }

/* ══════════════════════════════════════════════════════════════════════════════
   RESPONSIVE
   ══════════════════════════════════════════════════════════════════════════════ */
@media (max-width: 900px) {
    .map-location-float { width: 260px; top: 72px; right: 8px; }
    .map-legend-float { width: 260px; bottom: 88px; right: 8px; }
    .map-timeline-float { width: calc(100vw - 32px); bottom: 12px; }
    .map-sidebar-float { width: 180px; }
}
@media (max-width: 1024px) {
    .dashboard-layout { grid-template-columns: 1fr; }
    .metrics-grid { grid-template-columns: repeat(4, 1fr); }
    .analysis-row { grid-template-columns: 1fr; }
    .footer-container { grid-template-columns: 1fr 1fr; }
    .analysis-kpi-row { grid-template-columns: repeat(2, 1fr) !important; }
    .analysis-bottom { grid-template-columns: 1fr !important; }
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
@media (max-width: 600px) {
    .analysis-kpi-row { grid-template-columns: 1fr 1fr !important; }
}
"""