from .models import Menu, MenuName


def init_menu(*args):
    menu_name_1 = MenuName(name="menu_1")
    menu_name_1.save()

    menu_1 = Menu(label='Заголовок 1', url='/label1', menu_name=menu_name_1)
    menu_1.save()

    submenu_11 = Menu(label='Подзаголовок 11', url='/sub-label1', menu_name=menu_name_1, menu=menu_1)
    submenu_11.save()
    submenu_12 = Menu(label='Подзаголовок 12', url='/sub-label2', menu_name=menu_name_1, menu=menu_1)
    submenu_12.save()
    submenu_13 = Menu(label='Подзаголовок 13', url='/sub-label3', menu_name=menu_name_1, menu=menu_1)
    submenu_13.save()

    submenu_131 = Menu(label='Подзаголовок 131', url='/sub-sub-label1', menu_name=menu_name_1, menu=submenu_13)
    submenu_131.save()
    submenu_132 = Menu(label='Подзаголовок 132', url='/sub-sub-label2', menu_name=menu_name_1, menu=submenu_13)
    submenu_132.save()

    submenu_1311 = Menu(label='Подзаголовок 1311', url='/sub-sub-sub-label1', menu_name=menu_name_1, menu=submenu_131)
    submenu_1311.save()
    submenu_1312 = Menu(label='Подзаголовок 1312', url='/sub-sub-sub-label2', menu_name=menu_name_1, menu=submenu_131)
    submenu_1312.save()
    submenu_1313 = Menu(label='Подзаголовок 1313', url='/sub-sub-sub-label3', menu_name=menu_name_1, menu=submenu_131)
    submenu_1313.save()
    submenu_1314 = Menu(label='Подзаголовок 1314', url='/sub-sub-sub-label4', menu_name=menu_name_1, menu=submenu_131)
    submenu_1314.save()

    submenu_14 = Menu(label='Подзаголовок 14', url='/sub-label4', menu_name=menu_name_1, menu=menu_1)
    submenu_14.save()

    # Меню 2
    menu_name_2 = MenuName(name="menu_2")
    menu_name_2.save()

    menu_2 = Menu(label='Заголовок 2', url='/label2', menu_name=menu_name_2)
    menu_2.save()

    submenu_21 = Menu(label='Подзаголовок 21', url='/sub-label1', menu_name=menu_name_2, menu=menu_2)
    submenu_21.save()
    submenu_22 = Menu(label='Подзаголовок 22', url='/sub-label2', menu_name=menu_name_2, menu=menu_2)
    submenu_22.save()
    submenu_23 = Menu(label='Подзаголовок 23', url='/sub-label3', menu_name=menu_name_2, menu=menu_2)
    submenu_23.save()
    submenu_24 = Menu(label='Подзаголовок 24', url='/sub-label4', menu_name=menu_name_2, menu=menu_2)
    submenu_24.save()

    submenu_211 = Menu(label='Подзаголовок 211', url='/sub-sub-label1', menu_name=menu_name_2, menu=submenu_21)
    submenu_211.save()

    submenu_212 = Menu(label='Подзаголовок 212', url='/sub-sub-label2', menu_name=menu_name_2, menu=submenu_21)
    submenu_212.save()

    submenu_2111 = Menu(label='Подзаголовок 2111', url='/sub-sub-sub-label1', menu_name=menu_name_2, menu=submenu_211)
    submenu_2111.save()
    submenu_2112 = Menu(label='Подзаголовок 2112', url='/sub-sub-sub-label2', menu_name=menu_name_2, menu=submenu_211)
    submenu_2112.save()
    submenu_2113 = Menu(label='Подзаголовок 2113', url='/sub-sub-sub-label3', menu_name=menu_name_2, menu=submenu_211)
    submenu_2113.save()

