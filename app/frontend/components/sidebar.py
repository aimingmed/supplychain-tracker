from nicegui import ui
from nicegui.events import ValueChangeEventArguments

def create_sidebar(active_function: ui.state):
    """创建侧边栏导航
    
    Args:
        active_function: 当前活动功能的状态变量
    """
    with ui.column().classes('w-full h-full p-4 gap-2'):
        # 系统标题
        ui.label('生产管理系统').classes('text-xl font-bold mb-4')
        
        # 菜单项
        menu_items = [
            {'id': 'product', 'label': '产品管理', 'icon': 'inventory_2'},
            # {'id': 'inventory', 'label': '库存管理', 'icon': 'warehouse'},
            # {'id': 'task', 'label': '任务管理', 'icon': 'assignment'},
        ]
        
        for item in menu_items:
            is_active = active_function.value == item['id']
            ui.button(
                item['label'],
                on_click=lambda _, id=item['id']: active_function.set(id),
                icon=item['icon']
            ).props('flat').classes(
                f'w-full justify-start {"bg-blue-100 text-blue-600" if is_active else "text-gray-700 hover:bg-gray-100"}'
            )
