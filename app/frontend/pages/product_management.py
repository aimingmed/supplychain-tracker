from nicegui import ui
from datetime import datetime
from typing import Optional
from pages.routers import prod_router

from components.topbar import create_topbar
from components.sidebar import create_sidebar

@prod_router.page('/product-management')
def product_management_page():

    # Main content area with Element UI styling
    # ui.label('产品管理').classes('text-2xl font-bold mb-6 text-gray-800')
    
    # 数据筛选部分
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.column().classes('w-full gap-4'):
            ui.label('数据筛选').classes('text-lg font-medium text-gray-700')
            
            with ui.row().classes('w-full items-center gap-4'):
                ui.label('产品名称/编号：').classes('text-gray-600')
                ui.input(placeholder='产品名称/编号').classes('w-64')
                
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                ui.button('查询', icon='search').classes('text-white')
                ui.button('重置', icon='refresh').classes('text-gray-700').props('color=grey')
    
    # 数据展示部分
    with ui.dialog() as add_dialog, ui.card().style('width: 800px; max-width: none'):
        with ui.column().classes('w-full gap-4'):
            ui.label('添加产品').classes('text-lg font-medium text-gray-700')
            ui.separator()
            with ui.row().classes('w-full items-center gap-4'):
                ui.label('产品类型').classes('text-gray-600')
                ui.select({1: '产品', 2: '母液', 3: '原料', 4: '耗材'}, value=1).classes('w-64')
                ui.label('产品名称').classes('text-gray-600')
                ui.input(placeholder='请输入产品名称').classes('w-64')

            with ui.row().classes('w-full items-center gap-4'):
                ui.label('产品编号').classes('text-gray-600')
                ui.input(placeholder='请输入产品编号').classes('w-64')
                ui.label('产品单位').classes('text-gray-600')
                ui.select({1: 'μL', 2: 'mL', 3: 'L'}).classes('w-64')

            ui.label('规格').classes('text-lg font-medium text-gray-700')
            rows = [
                {
                    '需要': 1,
                    '名称': 'MasterAim®Primary Enhancer',
                    '浓度': 500,
                    '浓度单位': 'μL',
                    '用量': 100,
                    '用量单位':'μL',
                    '操作': '+',
                },
            ]
            
            ui.table(rows=rows).classes('w-full border rounded')

            ui.label('组分').classes('text-lg font-medium text-gray-700')

            
            ui.label('添加物').classes('text-lg font-medium text-gray-700')
            
            ui.textarea(placeholder='备注信息').style('width: 700px; max-width: none')

    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.row().classes('w-full justify-between items-center'):
            # Product type tabs
            prod_toggle = ui.toggle(['产品', '母液', '原料', '耗材'], value='产品')
            
            # Action buttons
            with ui.row().classes('gap-2'):
                ui.button('添加产品', icon='add', on_click=add_dialog.open)
                ui.button('修改产品', icon='edit')
                ui.button('删除产品', icon='delete').props('color=red')
                ui.button('历史产品', icon='history')
                ui.button(icon='autorenew').props('color=black')
    
    # 示例数据，之后可以从代码移除
    columns = [
        {'name': 'id', 'label': '序号', 'field': 'id', 'align': 'center', 'sortable': True},
        {'name': 'type', 'label': '产品类型', 'field': 'type', 'align': 'center'},
        {'name': 'name', 'label': '产品名称', 'field': 'name', 'align': 'center'},
        {'name': 'code', 'label': '产品编号', 'field': 'code', 'align': 'center'},
        {'name': 'spec', 'label': '规格', 'field': 'spec', 'align': 'center'},
        {'name': 'created', 'label': '添加时间', 'field': 'created', 'align': 'center'},
        {'name': 'updated', 'label': '修改时间', 'field': 'updated', 'align': 'center'},
        {'name': 'actions', 'label': '操作', 'field': 'act', 'align': 'center'},
    ]
    
    rows = [
        {
            'id': 1,
            'type': '产品',
            'name': 'MasterAim®Primary Enhancer',
            'code': '100-008',
            'spec': '500μL',
            'created': '2024-09-03',
            'updated': '',
            'act': '详情'
        },
        # Add more sample rows as needed
    ]
    
    ui.table(columns=columns, rows=rows, pagination=0).classes('w-full border rounded')
    
    
    # Header with Element UI blue theme
    create_topbar()
    
    # Sidebar with light background and subtle shadow
    create_sidebar()