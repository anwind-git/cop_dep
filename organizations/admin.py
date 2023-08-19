from django.contrib import admin
from .models import Organizations, RestaurantAddresses, Cities

admin.site.site_header = "Панель администратора"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в админку"


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ['name_restaurant']


@admin.register(RestaurantAddresses)
class RestaurantAddressesAdmin(admin.ModelAdmin):
    list_display = ['restaurant_addresse']


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ['city']
    prepopulated_fields = {'slug': ('city',)}



