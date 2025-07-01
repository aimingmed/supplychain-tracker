from nicegui import ui
from datetime import datetime
from typing import Optional
from pages.routers import prod_router

from components.topbar import create_topbar
from components.sidebar import create_sidebar
from components.fullcalendar import FullCalendar as fullcalendar

@prod_router.page('/task-management')
def task_management_page():

    # Main content area with Element UI styling
    # ui.label('任务管理').classes('text-2xl font-bold mb-6 text-gray-800')
    
    # Filter Section
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.column().classes('w-full gap-4'):
            ui.label('数据筛选').classes('text-lg font-medium text-gray-700')
            
            with ui.row().classes('w-full items-center gap-4'):
                ui.label('生产状态：').classes('text-gray-600')
                ui.input(placeholder='请选择').classes('w-64')
                ui.label('产品名称/编号：').classes('text-gray-600')
                ui.input(placeholder='产品名称/编号').classes('w-64')
                
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                ui.button('查询', icon='search').classes('text-white')
                ui.button('重置', icon='refresh').classes('text-gray-700').props('color=grey')
    
    # Product Type Tabs and Actions
    with ui.card().classes('w-full mb-6 shadow-sm'):
        with ui.tabs().classes('w-full') as tabs:
            task = ui.tab('任务视图')
            schedule = ui.tab('排班视图')
        with ui.tab_panels(tabs, value=task).classes('w-full'):
            
            with ui.tab_panel(task):
                with ui.row().classes('w-full justify-between items-center'):
                    # Product type tabs
                    prod_toggle = ui.toggle(['产品', '母液', '原料', '耗材'], value='产品')
                    
                    # Action buttons
                    with ui.row().classes('gap-2'):
                        ui.button('添加任务', icon='add_task')
                        ui.button('修改任务', icon='edit')
                        ui.button('合并任务', icon='join_full').props('color=green')
                        ui.button('分配任务', icon='assignment').props('color=red')
                        ui.button('入库审核', icon='assignment_turned_in')
                        ui.button(icon='autorenew').props('color=black')
                    # Data Table
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


            with ui.tab_panel(schedule):
                schedule_options = {
                    'initialView': 'dayGridMonth',
                    'headerToolbar': {'left': 'title', 'right': ''},
                    'footerToolbar': {'right': 'prev,next today'},
                    'slotMinTime': '05:00:00',
                    'slotMaxTime': '22:00:00',
                    'allDaySlot': False,
                    'timeZone': 'local',
                    'height': 'auto',
                    'width': 'auto',
                    'events': [
                        {
                            'title': '任务1',
                            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 08:00:00',
                            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
                            'color': 'red',
                        },
                        {
                            'title': '任务2',
                            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
                            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 12:00:00',
                            'color': 'green',
                        },
                    ],
                }

                fullcalendar(schedule_options)

    
    # Header with Element UI blue theme
    create_topbar()
    
    # Sidebar with light background and subtle shadow
    create_sidebar()