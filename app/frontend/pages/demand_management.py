from nicegui import ui
from datetime import datetime
from typing import Optional
from pages.routers import prod_router

from components.topbar import create_topbar
from components.sidebar import create_sidebar

@prod_router.page('/demand-management')
def demand_management_page():
    # Main content area with Element UI styling
    # ui.label('需求管理').classes('text-2xl font-bold mb-6 text-gray-800')
    
    # Filter Section
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.column().classes('w-full gap-4'):
            ui.label('数据筛选').classes('text-lg font-medium text-gray-700')
            
            with ui.row().classes('w-full items-center gap-4'):
                ui.label('需求编号：').classes('text-gray-600')
                ui.input(placeholder='需求编号').classes('w-64')
                ui.label('需求名称：').classes('text-gray-600')
                ui.input(placeholder='需求名称').classes('w-64')

            with ui.row().classes('w-full items-center gap-4'):
                ui.label('产品名称：').classes('text-gray-600')
                ui.input(placeholder='产品名称').classes('w-64')
                ui.label('提交时间：').classes('text-gray-600')
                with ui.input(placeholder='起止时间').classes('w-64') as date_input:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().props('range').bind_value(
                                date_input,
                                forward=lambda x: f'{x["from"]} - {x["to"]}' if x else None,
                                backward=lambda x: {
                                    'from': x.split(' - ')[0],
                                    'to': x.split(' - ')[1],
                                } if ' - ' in (x or '') else None,
                            ):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with date_input.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
                   
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                ui.button('查询', icon='search').classes('bg-blue-600 text-white')
                ui.button('重置', icon='refresh').classes('text-gray-700').props('color=grey')
    
    # Product Type Tabs and Actions
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.row().classes('w-full justify-between items-center'):
            # Product type tabs
            prod_toggle = ui.toggle(['需求统计', '产品统计'], value='需求统计')
            
            # Action buttons
            with ui.row().classes('gap-2'):
                ui.button(icon='autorenew').props('color=black')
    
    # Data Table
    columns = [
        {'name': 'id', 'label': '序号', 'field': 'id', 'align': 'center', 'sortable': True},
        {'name': 'code', 'label': '产品编号', 'field': 'code', 'align': 'center'},
        {'name': 'demand', 'label': '需求名称', 'field': 'demand', 'align': 'center'},
        {'name': 'name', 'label': '产品名称', 'field': 'name', 'align': 'center'},
        {'name': 'spec', 'label': '规格', 'field': 'spec', 'align': 'center'},
        {'name': 'quant', 'label': '数量', 'field': 'quant', 'align': 'center'},
        {'name': 'usage', 'label': '用途', 'field': 'usage', 'align': 'center'},
        {'name': 'submit', 'label': '提交时间', 'field': 'submit', 'align': 'center'},
        {'name': 'expected', 'label': '期望交付', 'field': 'expected', 'align': 'center'},
        {'name': 'organization', 'label': '客户单位', 'field': 'org', 'align': 'center'},
        {'name': 'client', 'label': '客户姓名', 'field': 'client', 'align': 'center'},
        {'name': 'location', 'label': '客户地址', 'field': 'loc', 'align': 'center'},
        {'name': 'shipment', 'label': '发货时间', 'field': 'ship', 'align': 'center'},
        {'name': 'progress', 'label': '生产进度', 'field': 'prog', 'align': 'center'},
        {'name': 'actions', 'label': '操作', 'field': 'act', 'align': 'center'},
    ]
    
    rows = [
        {
            'id': 1,
            'code': '100-008',
            'demand': '测试需求',
            'name': 'MasterAim®Primary Enhancer',
            'spec': '500μL',
            'quant': '100',
            'usage': '出售',
            'submit': '2025-07-11',
            'expected': '2025-07-12',
            'org': '艾名医学',
            'client': '邱旻',
            'loc': '杭州',
            'ship': '2025-07-13',
            'prog': '生产中',
            'act': '详情',
        },
        # Add more sample rows as needed
    ]
    
    ui.table(columns=columns, rows=rows).classes('w-full border rounded')
    
    # Pagination
    with ui.row().classes('w-full justify-between items-center mt-4'):
        ui.label('共 41 条').classes('text-gray-600')
        with ui.pagination(1, 5).classes('gap-1'):
            ui.button(icon='chevron_left')
            ui.button('1')
            ui.button('2')
            ui.button('3')
            ui.button('4')
            ui.button('5')
            ui.button(icon='chevron_right')

    
    # Header with Element UI blue theme
    create_topbar()
    
    # Sidebar with light background and subtle shadow
    create_sidebar()