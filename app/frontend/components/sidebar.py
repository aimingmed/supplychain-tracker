from nicegui import ui

def create_sidebar():
    with ui.left_drawer(fixed=True, top_corner=True).classes('bg-white w-64 h-full shadow-md'):
        with ui.column().classes('w-full h-full bg-white'):
            # Logo section
            with ui.row():
                ui.image('https://tutor.aimingmed.com/file/assets/logo.png').classes('w-20')
                ui.button(icon='menu').props('flat')
            
            # Menu section with scroll
            with ui.scroll_area().classes('w-full h-[calc(100vh-64px)]'):
                with ui.column().classes('w-full p-2'):
                    # Production Management section
                    with ui.expansion('生产管理', icon='factory').classes('w-full text-gray-700'):
                        ui.link('产品管理', 'product-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
                        ui.link('库存管理', 'inventory-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
                        ui.link('需求管理', 'demand-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
                        ui.link('任务管理', 'task-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
                        ui.link('物料管理', 'material-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
                        ui.link('余料管理', 'scrap-management').classes('w-full pl-8 py-2 hover:bg-blue-50')
