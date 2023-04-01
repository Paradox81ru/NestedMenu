from django.test import TestCase
from .helper import init_menu
from .models import Menu, MenuName


class TestMenu(TestCase):

    def test_save_menu(self):
        """
        Тестирует, чтобы при изменении Имени меню у одного подменю,
        так же обязательно поменялись бы Имени меню и всех его вложенных подменю,
        и таким образом чтобы всё подменю корректно перенеслось из меню одного имени в другое.
         """
        menus = Menu.objects.all()
        self.assertTrue(menus.count() > 0)
        menu_21 = Menu.objects.get(label="Подзаголовок 21")
        # Проверяю, что меню принадлежит к имени меню 2
        self.assertEqual(menu_21.menu_name_id, 2)
        menu_name_1 = MenuName.objects.get(pk=1)
        # Меняю его на второе меню,
        menu_21.menu_name = menu_name_1
        menu_21.save()
        # и проверяю, что имя меню сменилось.
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