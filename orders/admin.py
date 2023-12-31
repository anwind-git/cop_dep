from django.contrib import admin
from .models import ShippingAddresses, Orders, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


@admin.register(ShippingAddresses)
class ShippingAddressesAdmin(admin.ModelAdmin):
    list_display = ['addresse']
    search_fields = ['addresse']
    list_per_page = 15
