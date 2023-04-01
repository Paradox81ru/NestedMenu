from django.contrib import admin

from .models import Menu, MenuName


@admin.register(MenuName)
class MenuNameAdmin(admin.ModelAdmin):
    pass


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name', 'menu_label', 'menu')
    list_select_related = ('menu_name', 'menu')
    list_display_links = ('menu_label',)
    list_filter = ('menu_name',)
    search_fields = ('label', 'menu__label')

    class Media:
        # Добавляю в форму админки скрипт, чтобы изменять список подменю в соответствии с выбором Имени меню.
        js = ('admin/js/menu_restriction.js',)

    @admin.display(description='Метка/ссылка', ordering='label')
    def menu_label(self, obj):
        return f'{obj.label} - {obj.url}'
