from nicegui import ui
from datetime import datetime
from typing import Optional
from pages.routers import prod_router

from components.topbar import create_topbar
from components.sidebar import create_sidebar

@prod_router.page('/scrap-management')
def scrap_management_page():

    # Main content area with Element UI styling
    # ui.label('余料管理').classes('text-2xl font-bold mb-6 text-gray-800')
    
    # Filter Section
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.column().classes('w-full gap-4'):
            ui.label('数据筛选').classes('text-lg font-medium text-gray-700')
            
            with ui.row().classes('w-full items-center gap-4'):
                ui.label('登记人：').classes('text-gray-600')
                ui.input(placeholder='选择登记人').classes('w-64')
                ui.label('产品名称/编号：').classes('text-gray-600')
                ui.input(placeholder='产品名称/编号').classes('w-64')
                
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                ui.button('查询', icon='search').classes('text-white')
                ui.button('重置', icon='refresh').classes('text-gray-700').props('color=grey')
    
    # Product Type Tabs and Actions
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.row().classes('w-full justify-between items-center'):
            # Product type tabs
            prod_toggle = ui.toggle(['产品', '母液'], value='产品')
            
            # Action buttons
            with ui.row().classes('gap-2'):
                ui.button(icon='autorenew').props('color=black')
    
    # Data Table
    columns = [
        {'name': 'id', 'label': '序号', 'field': 'id', 'align': 'center', 'sortable': True},
        {'name': 'query', 'label': '申领编号', 'field': 'query', 'align': 'center'},
        {'name': 'type', 'label': '任务类型', 'field': 'type', 'align': 'center'},
        {'name': 'name', 'label': '产品名称', 'field': 'name', 'align': 'center'},
        {'name': 'material', 'label': '物料列表', 'field': 'material', 'align': 'center'},
        {'name': 'code', 'label': '物料编号', 'field': 'code', 'align': 'center'},
        {'name': 'quant', 'label': '数量', 'field': 'quant', 'align': 'center'},
        {'name': 'unit', 'label': '单位', 'field': 'unit', 'align': 'center'},
        {'name': 'apply', 'label': '申请人', 'field': 'apply', 'align': 'center'},
        {'name': 'date', 'label': '申请时间', 'field': 'date', 'align': 'center'},
        {'name': 'check', 'label': '审核时间', 'field': 'check', 'align': 'center'},
        {'name': 'status', 'label': '当前状态', 'field': 'status', 'align': 'center'},
        {'name': 'actions', 'label': '操作', 'field': 'act', 'align': 'center'},
    ]
    
    rows = [
        {
            'id': 1,
            'query': 'Q123',
            'type': '产品',
            'name': 'MasterAim®Primary Enhancer',
            'material': 'MAM-MB001',
            'code': '100-008',
            'quant': 500,
            'unit': 'μL',
            'apply': '邱旻',
            'date': '2024-09-03',
            'check': '2024-09-04',
            'status': '已申领',
            'act': '详情'
        },
        # Add more sample rows as needed
    ]
    
    ui.table(columns=columns, rows=rows, selection='single', pagination=0).classes('w-full border rounded')
    
    
    # Header with Element UI blue theme
    create_topbar()
    
    # Sidebar with light background and subtle shadow
    create_sidebar()