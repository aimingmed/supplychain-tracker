from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from typing import Optional

from components.topbar import create_topbar
from components.sidebar import create_sidebar

# Import all pages to register their routes
from pages import (
    product_management,
    # inventory_management,
    # demand_management,
    # task_management,
    # material_management,
    # scrap_management
)

# Apply Element UI inspired global styles
# ui.add_css("styles/element.css")

@ui.page('/')
def main_page():
    # Main content area with Element UI styling
    with ui.column().classes('w-[calc(100%-16rem)] h-full p-6'):
        ui.label('生产系统示例').classes('text-2xl font-bold text-[#303133] mb-2')
        ui.label('选择左侧的生产菜单项').classes('text-[#909399]')
    
    # Header with Element UI blue theme
    with ui.header().classes('justify-between items-center h-16 bg-[#409EFF] text-white px-4 shadow-sm'):
        create_topbar()
    
    # Sidebar with light background and subtle shadow
    with ui.left_drawer(fixed=True, top_corner=True).classes('bg-white w-64 h-full shadow-md'):
        create_sidebar()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Production Management", 
        favicon="🏭", 
        reload=True,
        dark=False  # Force light mode to match Element UI
    )
