from nicegui import ui
from nicegui.events import ValueChangeEventArguments

def create_sidebar():
    with ui.column().classes('w-full'):
        # Production Management Menu
        with ui.expansion('生产管理', icon='factory').classes('w-full'):
            ui.link('产品管理', '/product-management').classes('w-full pl-8')
            ui.link('库存管理', '/inventory-management').classes('w-full pl-8')
            ui.link('需求管理', '/demand-management').classes('w-full pl-8')
            ui.link('任务管理', '/task-management').classes('w-full pl-8')
            ui.link('物料管理', '/material-management').classes('w-full pl-8')
            ui.link('余料管理', '/scrap-management').classes('w-full pl-8')
