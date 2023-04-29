from typing import Final

from django.test import TestCase
# from .helper import init_menu
from .models import Menu, MenuName
from .templatetags.draw_menu import _get_list_group_submenu, _get_struct_menu, _set_show_marker


class TestMenu(TestCase):
    MENU_LIST: Final = [
        {'id': 1, 'label': 'Заголовок 1', 'url': '/label1', 'menu_id': None},
        {'id': 2, 'label': 'Подзаголовок 11', 'url': '/sub-label1', 'menu_id': 1},
        {'id': 3, 'label': 'Подзаголовок 12', 'url': '/sub-label2', 'menu_id': 1},
        {'id': 4, 'label': 'Подзаголовок 13', 'url': '/sub-label3', 'menu_id': 1},
        {'id': 5, 'label': 'Подзаголовок 131', 'url': '/sub-sub-label1', 'menu_id': 4},
        {'id': 6, 'label': 'Подзаголовок 132', 'url': '/sub-sub-label2', 'menu_id': 4},
        {'id': 7, 'label': 'Подзаголовок 1311', 'url': '/sub-sub-sub-label1', 'menu_id': 5},
        {'id': 8, 'label': 'Подзаголовок 1312', 'url': '/sub-sub-sub-label2', 'menu_id': 5},
        {'id': 9, 'label': 'Подзаголовок 1313', 'url': '/sub-sub-sub-label3', 'menu_id': 5},
        {'id': 10, 'label': 'Подзаголовок 1314', 'url': '/sub-sub-sub-label4', 'menu_id': 5},
        {'id': 11, 'label': 'Подзаголовок 14', 'url': '/sub-label4', 'menu_id': 1}]

    STRUCT_MENU: Final = \
        {'id': 1, 'label': 'Заголовок 1', 'url': '/menu/label1', 'menu_id': None, 'items': [
            {'id': 2, 'label': 'Подзаголовок 11', 'url': '/menu/label1/sub-label1', 'menu_id': 1},
            {'id': 3, 'label': 'Подзаголовок 12', 'url': '/menu/label1/sub-label2', 'menu_id': 1},
            {'id': 4, 'label': 'Подзаголовок 13', 'url': '/menu/label1/sub-label3', 'menu_id': 1, 'items': [
                {'id': 5, 'label': 'Подзаголовок 131', 'url': '/menu/label1/sub-label3/sub-sub-label1', 'menu_id': 4,
                 'items': [
                     {'id': 7, 'label': 'Подзаголовок 1311',
                      'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label1', 'menu_id': 5},
                     {'id': 8, 'label': 'Подзаголовок 1312',
                      'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label2', 'menu_id': 5},
                     {'id': 9, 'label': 'Подзаголовок 1313',
                      'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label3', 'menu_id': 5},
                     {'id': 10, 'label': 'Подзаголовок 1314',
                      'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label4', 'menu_id': 5}]},
                {'id': 6, 'label': 'Подзаголовок 132', 'url': '/menu/label1/sub-label3/sub-sub-label2', 'menu_id': 4}]},
            {'id': 11, 'label': 'Подзаголовок 14', 'url': '/menu/label1/sub-label4', 'menu_id': 1}]}

    @classmethod
    def setUpClass(cls):
        # При миграции базы данных уже создаётся тестовое меню, на основании которого и происходит тестирование.
        # В противном случае надо раскомментировать init_menu() для создания тестового меню.
        # init_menu()
        super().setUpClass()

    def test_get_list_group_submenu(self):
        """ Проверяет группировку списка подменю """
        expected_group_list: Final = {
            1: [{'id': 2, 'label': 'Подзаголовок 11', 'url': '/sub-label1', 'menu_id': 1},
                {'id': 3, 'label': 'Подзаголовок 12', 'url': '/sub-label2', 'menu_id': 1},
                {'id': 4, 'label': 'Подзаголовок 13', 'url': '/sub-label3', 'menu_id': 1},
                {'id': 11, 'label': 'Подзаголовок 14', 'url': '/sub-label4', 'menu_id': 1}],
            4: [{'id': 5, 'label': 'Подзаголовок 131', 'url': '/sub-sub-label1', 'menu_id': 4},
                {'id': 6, 'label': 'Подзаголовок 132', 'url': '/sub-sub-label2', 'menu_id': 4}],
            5: [{'id': 7, 'label': 'Подзаголовок 1311', 'url': '/sub-sub-sub-label1', 'menu_id': 5},
                {'id': 8, 'label': 'Подзаголовок 1312', 'url': '/sub-sub-sub-label2', 'menu_id': 5},
                {'id': 9, 'label': 'Подзаголовок 1313', 'url': '/sub-sub-sub-label3', 'menu_id': 5},
                {'id': 10, 'label': 'Подзаголовок 1314', 'url': '/sub-sub-sub-label4', 'menu_id': 5}]
        }
        group_list = _get_list_group_submenu(self.MENU_LIST)
        self.assertEqual(group_list, expected_group_list)

    def test_get_struct_menu(self):
        """ Проверяет формирование структурированного меню """
        expected_struct_menu: Final = self.STRUCT_MENU
        struct_menu = _get_struct_menu(self.MENU_LIST)
        self.assertEqual(struct_menu, expected_struct_menu)

    def test_set_show_marker(self):
        struct_menu = dict(self.STRUCT_MENU)
        url_path = "/menu/label1/sub-label1/sub-sub-label1/sub-sub-sub-label1"
        url_begin_path = "/menu/label1/sub-label1/sub-sub-label1"
        expected_marked_struct_menu: Final = \
           {'id': 1, 'label': 'Заголовок 1', 'url': '/menu/label1', 'menu_id': None, 'items': [
               {'id': 2, 'label': 'Подзаголовок 11', 'url': '/menu/label1/sub-label1', 'menu_id': 1, 'is_show': True},
               {'id': 3, 'label': 'Подзаголовок 12', 'url': '/menu/label1/sub-label2', 'menu_id': 1, 'is_show': True},
               {'id': 4, 'label': 'Подзаголовок 13', 'url': '/menu/label1/sub-label3', 'menu_id': 1, 'items': [
                   {'id': 5, 'label': 'Подзаголовок 131', 'url': '/menu/label1/sub-label3/sub-sub-label1', 'menu_id': 4, 'items': [
                       {'id': 7, 'label': 'Подзаголовок 1311', 'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label1', 'menu_id': 5},
                       {'id': 8, 'label': 'Подзаголовок 1312', 'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label2', 'menu_id': 5},
                       {'id': 9, 'label': 'Подзаголовок 1313', 'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label3', 'menu_id': 5},
                       {'id': 10, 'label': 'Подзаголовок 1314', 'url': '/menu/label1/sub-label3/sub-sub-label1/sub-sub-sub-label4', 'menu_id': 5}], 'is_show': False},
                   {'id': 6, 'label': 'Подзаголовок 132', 'url': '/menu/label1/sub-label3/sub-sub-label2', 'menu_id': 4, 'is_show': False}], 'is_show': True},
               {'id': 11, 'label': 'Подзаголовок 14', 'url': '/menu/label1/sub-label4', 'menu_id': 1, 'is_show': True}], 'is_show': True}
        _set_show_marker(struct_menu, url_path, url_begin_path)
        self.assertEqual(struct_menu, expected_marked_struct_menu)

    def test_save_menu(self):
        """
        Тестирует, чтобы при изменении Имени меню у одного подменю,
        так же обязательно поменялись бы Имени меню и всех его вложенных подменю,
        и таким образом чтобы всё подменю корректно перенеслось из меню одного имени в другое.
         """
        menus = Menu.objects.all()
        self.assertTrue(menus.count() > 0)
        menu_21 = Menu.objects.get(label="Подзаголовок 21")
        # Проверяю, что меню принадлежит к имени меню 2.
        self.assertEqual(menu_21.menu_name_id, 2)
        # Нахожу меню из Имени меню 1
        menu_1 = Menu.objects.get(label="Заголовок 1")
        self.assertEqual(menu_1.menu_name_id, 1)
        menu_name_1 = MenuName.objects.get(name="menu_1")
        # передаю подменю из Имени меню 2 в меню из Имени меню 1,
        menu_21.menu_name = menu_name_1
        menu_21.menu = menu_1
        menu_21.save()
        menu_21 = Menu.objects.get(label="Подзаголовок 21")
        # и проверяю, что Имя меню сменилось.
        self.assertEqual(menu_21.menu_name_id, 1)
        # Нахожу первое значение подменю,
        sub_menu = menu_21.submenu.first()
        # и проверяю что у него номер меню тоже первый.
        self.assertEqual(sub_menu.menu_name_id, 1)
        # Более того, нахожу теперь уже его подменю,
        sub_sub_menu = sub_menu.submenu.all()
        # и убеждаюсь, что все его подменю тоже теперь относятся к первому меню.
        for menu in sub_sub_menu:
            self.assertEqual(menu.menu_name_id, 1)

    def test_save_self(self):
        """
        Тестирует невозможность сохранения меню при передаче меню самому себе
        или передачи подменю из другого Имени меню.
        """
        menu_132 = Menu.objects.get(label="Подзаголовок 132")
        belong_menu_132 = menu_132.menu
        # Пытаюсь назначить меню самому себе.
        menu_132.menu = menu_132
        menu_132.save()
        # Снова нахожу меню,
        menu_132 = Menu.objects.get(label="Подзаголовок 132")
        # но изменения произойти не должны,
        self.assertNotEqual(menu_132.id, menu_132.menu.id)
        self.assertEqual(menu_132.menu_id, belong_menu_132.id)

        # Нахожу подменю из Имени меню 2.
        menu_23 = Menu.objects.get(label="Подзаголовок 23")
        # и убеждаюсь, что у него нет подменю.
        self.assertEqual(menu_23.submenu.all().count(), 0)
        # Нахожу меню, которому принадлежит подменю 132.
        menu_13 = menu_132.menu
        # Проверяю, что меню_23 и меню_132 находятся в разных Именах меню,
        self.assertNotEqual(menu_23.menu_name_id, menu_132.menu_name_id)
        # и пытаюсь назначить подменю из Имени меню 1, подменю из Имени меню 2.
        menu_132.menu = menu_23
        # Сохраняю изменения.
        menu_132.save()

        menu_23 = Menu.objects.get(label="Подзаголовок 23")
        menu_132 = Menu.objects.get(label="Подзаголовок 132")
        # Далее проверяю, что ничего не изменилось, в меню_23 не появились подменю
        self.assertEqual(menu_23.submenu.all().count(), 0)
        # а меню_132 принадлежит тому же подменю что и ранее.
        self.assertEqual(menu_132.menu, menu_13)
