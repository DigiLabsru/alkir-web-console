# import hashlib

from nicegui import app, ui

# from ..styles.global_styles import apply_global_styles
# from ..styles.login_styles import apply_login_styles


def create_login_page():
    ui.colors(primary="#88B236")
    ui.add_head_html('''
        <style>
            body {
                height: 100vh;  /* Используем viewport height */
                background: #141414;
            }
            .nicegui-content {
                height: 100vh !important;
            }
        </style>
    ''')
    with ui.element().classes('w-full h-full flex justify-center items-center'):
        with ui.card().classes('w-[20%] p-8 bg-[#1F1F1F] rounded-lg'):
            ui.label('Авторизация').classes('text-2xl text-[#88B236] w-full text-center')
            login = ui.input(label='Логин', placeholder='Введите логин').classes('w-full').props('outlined')
            password = ui.input(label='Пароль', placeholder='Введите пароль', password=True).classes('w-full').props('outlined')
            ui.button('Войти', on_click=lambda: handle_login(login=login, password=password)).classes('w-full')


def handle_login(login, password):
    from ..main import user_list
    flag: bool = False
    for one_user in user_list.user_list:
        if one_user.login == login.value and one_user.pwd == password.value:
            flag = True
    if flag is True:
        app.storage.user.update({'username': login.value, 'authenticated': True})
        ui.navigate.to('/')
    else:
        ui.notify('Неправильный логин и/или пароль', color='negative')
