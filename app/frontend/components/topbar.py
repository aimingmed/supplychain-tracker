from nicegui import ui

def create_topbar():
    with ui.header().classes('justify-between items-center h-16 bg-[#409EFF] text-white px-4 shadow-sm'):
        ui.label('数字类器官模型（Digital Organoid ModelS, DOMS）').classes('text-lg font-medium')
        
        with ui.row().classes('items-center gap-2'):
            # Help dropdown
            with ui.dropdown_button('帮助', icon='help'):
                ui.item(text='插件下载').classes('w-40')
            
            # Notifications
            with ui.dropdown_button('通知', icon='notifications'):
                ui.item(text='消息列表').classes('w-40')
                ui.separator()
                ui.item(text='消息盒').classes('w-40')
            
            # User dropdown
            with ui.avatar('img:https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png'):
                with ui.menu().classes('w-48'):
                    with ui.column().classes('items-center p-4'):
                        ui.image('https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png').classes('w-12 h-12 rounded-full')
                        ui.label('生产管理员').classes('text-lg mt-2')
                    ui.menu_item('个人资料')
                    ui.menu_item('注销')
