import os
from uuid import uuid4

from fastapi import Request
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import app, ui
from starlette.middleware.base import BaseHTTPMiddleware

from .common.interface.ras.java_runtime import init_jvm, shutdown_jvm
from .common.schemas.settings import StartSettings, UserList
from .pages.login_page import create_login_page
from .pages.main_page import create_main_page

unrestricted_page_routes = {'/login'}
web_rac_token_dict: list = []
root_path = os.path.dirname(os.path.abspath(__file__))
user_groups: dict = {}
java_run: dict = {}

logger.info('Старт приложения')
start_settings: dict = {}
if "SETTINGS".upper() not in os.environ:
    logger.critical("В окружении не найдена переменная 'SETTINGS'")
    raise SystemExit(1)
else:
    try:
        variable_from_env = os.environ["SETTINGS".upper()]
        start_settings = (StartSettings.model_validate_json(variable_from_env))
        logger.info('Разбор переменной "SETTINGS" из окружения прошел успешно')
    except Exception as e:
        logger.critical(f'Ошибка разбора переменной "SETTINGS"\nТекст ошибки:\n{e}')
        raise SystemExit(1)
if "USER_LIST".upper() not in os.environ:
    logger.critical("В окружении не найдена переменная 'USER_LIST'")
    raise SystemExit(1)
else:
    try:
        variable_from_env: str = os.environ["USER_LIST".upper()]
        user_list = (UserList.model_validate_json(variable_from_env))
        logger.info('Разбор переменной "USER_LIST" из окружения прошел успешно')
    except Exception as e:
        logger.critical(f'Ошибка разбора переменной "USER_LIST"\nТекст ошибки:\n{e}')
        raise SystemExit(1)


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/')
def main_interface():
    create_main_page()


@ui.page('/login')
def login_interface():
    create_login_page()


@ui.page('/logout')
def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to('/login')


ui.run_with(
    app,
    storage_secret=str(uuid4()),
    title='Alkir web console',
    dark=True,
    favicon='🛠'
)


@app.on_startup
async def startup():
    global java_run
    java_run = init_jvm(root_path)


@app.on_shutdown
async def shutdown():
    shutdown_jvm()
