from loguru import logger
from nicegui import ui

from ..data.gen_menu_data import gen_menu_data
from .update_main import update_main


def update_tree(server: str, containers: dict):
    """Обновляет дерево для выбранного сервера"""
    containers['tree_container'].clear()
    with containers['tree_container'].classes('justify-center items-center'):
        ui.spinner('gears', size='6em')
    ui.timer(0.5, once=True, callback=lambda: load_data(containers=containers, server=server))


async def load_data(containers, server):
    # main_container = containers['tree_container']
    try:
        menu_data = gen_menu_data(server)
    except Exception as ex:
        ui.notify(ex, type='negative', position='top-right')
        logger.error(ex)
        containers['root_select'].clear()
        containers['tree_container'].clear()
        containers['main_container'].clear()
        return
    containers['tree_container'].clear()
    with containers['tree_container'].classes('justify-start items-start'):
        ui.tree(
            menu_data,
            node_key='id',
            label_key='text',
            on_select=lambda e: update_main(id=e.value, main_container=containers['main_container'], server=server)
        ).classes('self-start')
        # .classes('custom-tree w-full text-#88B236')
