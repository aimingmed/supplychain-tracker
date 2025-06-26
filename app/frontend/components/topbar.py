from nicegui import ui

def create_topbar():
    with ui.row().classes('w-full items-center justify-between p-2 bg-blue-800 text-white'):
        ui.label('Production Management System').classes('text-xl font-bold')
        
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='notifications', color='white').props('flat')
            ui.button(icon='account_circle', color='white').props('flat')
