from django.db import models


class MenuName(models.Model):
    name = models.CharField("Наименование меню", max_length=255, unique=True)

    class Meta:
        verbose_name = 'Наименование меню'
        verbose_name_plural = 'Наименование меню'
        db_table = "menu_menu_name"

    def __str__(self):
        return self.name


class Menu(models.Model):
    label = models.CharField("Метка", max_length=255)
    url = models.CharField("Ссылка", max_length=255)
    menu = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='submenu', verbose_name='принадлежит пункту меню')
    menu_name = models.ForeignKey(MenuName, on_delete=models.CASCADE, verbose_name='наименование меню')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None ):
        super().save(force_insert, force_update, using, update_fields)
        self.related_item_menu_name_save(self)

    def related_item_menu_name_save(self, item: 'Menu'):
        """ При сохранении меню проверят, если у принадлежащих ему подменю не совпадает Имя меню со своим,
            то меняет всем подменю и под-подменю Имя меню на такое же, как и у него.
         """
        submenu = item.submenu.all()
        if len(submenu) != 0 and submenu[0].menu_name != item.menu_name:
            item.submenu.update(menu_name=item.menu_name)
            for item in item.submenu.all():
                self.related_item_menu_name_save(item)

    def __str__(self):
        return f"{self.menu_name}: {self.label} - {self.url}"