from nicegui import ui
from datetime import datetime
from typing import Optional

@ui.page('/product-management')
def product_management_page():
    ui.label('产品管理').classes('text-2xl font-bold mb-4')
    
    # Filter Section
    with ui.card().classes('w-full mb-4'):
        with ui.row().classes('w-full items-center gap-4'):
            ui.input('产品名称', placeholder='输入产品名称')
            ui.input('产品编码', placeholder='输入产品编码')
            ui.date(value=datetime.now().date()).props('range')
            ui.button('搜索', icon='search')
            ui.button('重置', icon='refresh')
    
    # Data Table Section
    with ui.card().classes('w-full'):
        columns = [
            {'name': 'product_id', 'label': '产品ID', 'field': 'product_id'},
            {'name': 'name', 'label': '产品名称', 'field': 'name'},
            {'name': 'spec', 'label': '规格', 'field': 'spec'},
            {'name': 'quantity', 'label': '库存数量', 'field': 'quantity'},
            {'name': 'actions', 'label': '操作', 'field': 'actions'},
        ]
        rows = [
            {
                'product_id': 'P001',
                'name': '示例产品',
                'spec': '标准',
                'quantity': 100,
                'actions': '编辑 删除'
            }
        ]
        ui.table(columns=columns, rows=rows, row_key='product_id').classes('w-full')
        
        with ui.row().classes('w-full justify-between mt-4'):
            ui.label('共 1 条数据')
            ui.pagination(1, 1, 1)
