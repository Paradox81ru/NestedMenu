from django import template

from menu.models import Menu

register = template.Library()


@register.inclusion_tag("menu/fragments/nested_menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """ Тэг отображения меню """
    result = {"menu_name": menu_name}
    menu = Menu.objects.filter(menu_name__name=menu_name).values('id', 'label', 'url', 'menu_id')
    if len(menu) == 0:
        result['error'] = f'Меню {menu_name} не найдено'
    else:
        struct_menu = _get_struct_menu(menu)

        url_path = context['request'].path
        url_path_begin = url_path[:url_path.rfind("/")]
        _set_show_marker(struct_menu, url_path, url_path_begin)
        result["menu"] = [struct_menu]
    return result


def _get_struct_menu(menu: list):
    """
    Формирует структурированное меню

    :param menu: список меню из запроса.
    :param url_path: текущий URL
    :return: структурированное меню
    """
    list_group_submenu = _get_list_group_submenu(menu)
    item_menu = dict(menu[0])
    item_menu['url'] = '/menu' + item_menu['url']
    _set_submenu(item_menu, list_group_submenu)
    return item_menu


def _add_path(list_group, path):
    """ Добавляет путь от URL в начало ссылок каждого подменю """
    for item in list_group:
        item['url'] = path + item['url']
    return list_group


def _set_submenu(item_menu, list_group_submenu):
    """ Добавляет списки подменю в меню """
    if item_menu['id'] in list_group_submenu:
        item_menu['items'] = _add_path(list_group_submenu[item_menu['id']], item_menu['url'])
        for item in item_menu["items"]:
            _set_submenu(item, list_group_submenu)


def _set_show_marker(item_menu, url_path, url_path_begin: str):
    """ Устанавливает маркер видимости меню и подменю """
    # Если ссылка меню совпадает с текущей ссылкой,
    if item_menu['url'] == url_path:
        # значит выбран текущий элемент.
        item_menu['current_item'] = True
    item_menu['is_show'] = url_path_begin.startswith(item_menu['url'][:item_menu['url'].rfind("/")])
    if item_menu['is_show'] and 'items' in item_menu:
        for item in item_menu['items']:
            _set_show_marker(item, url_path, url_path_begin)


def _get_list_group_submenu(menu: list):
    """ Возвращает сгруппированный список подменю """
    list_group_submenu = {}
    for item in menu:

        if item['menu_id'] is not None:
            if item['menu_id'] in list_group_submenu:
                list_group_submenu[item['menu_id']].append(dict(item))
            else:
                list_group_submenu[item['menu_id']] = [dict(item)]
    return list_group_submenu
