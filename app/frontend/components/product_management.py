from nicegui import ui

def create_product_management():
    """产品管理组件"""
    with ui.column().classes('w-full p-4 gap-4'):
        # 标题和操作按钮
        with ui.row().classes('w-full justify-between items-center'):
            ui.label('产品管理').classes('text-2xl font-bold')
            with ui.row().classes('gap-2'):
                ui.button('新增产品', icon='add').classes('bg-blue-500 text-white')
                ui.button('导入', icon='upload').classes('bg-green-500 text-white')
        
        # 搜索和筛选区域
        with ui.card().classes('w-full p-4'):
            with ui.row().classes('w-full items-center gap-4'):
                ui.input(placeholder='搜索产品名称/编号').classes('flex-grow')
                ui.select(['全部类型', '产品', '母液', '原料'], value='全部类型')
                ui.button('搜索', icon='search').classes('bg-blue-500 text-white')
        
        # 数据表格
        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
            {'name': 'name', 'label': '产品名称', 'field': 'name'},
            {'name': 'code', 'label': '产品编号', 'field': 'code'},
            {'name': 'type', 'label': '类型', 'field': 'type'},
            {'name': 'actions', 'label': '操作', 'field': 'actions'},
        ]
        rows = [
            {'id': 1, 'name': '产品A', 'code': 'P001', 'type': '产品', 'actions': '编辑 删除'},
            {'id': 2, 'name': '原料B', 'code': 'M002', 'type': '原料', 'actions': '编辑 删除'},
        ]
        ui.table(columns=columns, rows=rows).classes('w-full')
