from nicegui import ui

from src.common.components import apply_theme, footer, hero_background, navbar
from .widgets import render_login_content

def register():
    @ui.page('/login')
    def login_page():
        apply_theme()
        
        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/login')
            
            with ui.element('div').classes('page-content content-wrapper'):
                render_login_content()
                
            footer()
