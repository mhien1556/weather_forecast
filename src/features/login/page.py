from nicegui import ui

from src.common.components import apply_theme, hero_background, navbar
from .widgets import render_login_content

def register():
    @ui.page('/login')
    def login_page():
        apply_theme()
        
        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/login')
            
            # Không dùng content-wrapper để card căn giữa toàn màn hình
            with ui.element('div').style(
                'display:flex; align-items:center; justify-content:center;'
                'min-height:calc(100vh - 70px); padding: 2rem; box-sizing:border-box;'
            ):
                render_login_content()
