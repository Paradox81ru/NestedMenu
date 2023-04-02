from django.test import TestCase
from .helper import init_menu
from .models import Menu, MenuName


class TestMenu(TestCase):

    @classmethod
    def setUpClass(cls):
        # При миграции базы данных уже создаётся тестовое меню, на основании которого и происходит тестирование.
        # В противном случае надо раскомментировать init_menu() для создания тестового меню.
        # init_menu()
        super().setUpClass()

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
