from django.contrib import admin
from .models import Professions, FormPayment, Employees


@admin.register(FormPayment)
class FormPaymentAdmin(admin.ModelAdmin):
    list_display = ['form_payment']


@admin.register(Professions)
class ProfessionsAdmin(admin.ModelAdmin):
    list_display = ['profession']


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    # Отображаемые поля
    list_display = ['last_name', 'first_name', 'phone', 'status1', 'salary']
    # Количество строк на странице
    list_per_page = 10
    # Поля по которым ведется поиск
    search_fields = ['last_name', 'first_name', 'INN', 'phone']
    # Фильтр по полям
    list_filter = ['status1', 'job']
