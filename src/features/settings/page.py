from nicegui import ui

from src.common.components import apply_theme, footer, hero_background, navbar
from .widgets import render_settings_content

def register():
    @ui.page('/settings')
    def settings_page():
        apply_theme()
        
        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/settings')
            
            with ui.element('div').classes('page-content content-wrapper'):
                with ui.element('div').classes('page-header'):
                    ui.label('Cài đặt hệ thống').classes('text-h4').style('font-weight:700;margin:0')
                    ui.label('Tùy chỉnh giao diện và sở thích cá nhân.').style('opacity:0.7')
                
                render_settings_content()
                
            footer()
