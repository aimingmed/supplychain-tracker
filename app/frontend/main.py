from nicegui import ui
from typing import Dict, Callable

from components.topbar import create_topbar
from components.sidebar import create_sidebar
from components.product_management import create_product_management

# 功能组件映射
FUNCTION_COMPONENTS: Dict[str, Callable] = {
    'product': create_product_management,
    # 'inventory': create_inventory_management,
    # 'task': create_task_management,
}

@ui.page('/')
def main_page():
    # 当前活动功能
    active, active_function = ui.state('product')
    
    # 主布局
    with ui.column().classes('w-full h-screen'):
        # 顶部导航栏
        with ui.header().classes('h-16 bg-blue-500 text-white shadow-md'):
            create_topbar()
        
        # 侧边栏
        with ui.left_drawer(fixed=True).classes('w-64 h-full bg-gray-50 shadow-md'):
            create_sidebar(active_function)

        # 主体内容
        with ui.row().classes('w-full h-[calc(100vh-4rem)]'):
            
            # 主内容区
            with ui.column().classes('flex-grow p-6 overflow-auto'):
                # 动态加载功能组件
                def render_content():
                    FUNCTION_COMPONENTS[active_function.value]()
                
                render_content()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Production Management", 
        favicon="🏭", 
        reload=True,
        dark=False  # Force light mode to match Element UI
    )
