from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'shop'

urlpatterns = [
    path('', ProductsHome.as_view(), name='shop'),
    path('<slug>', ProductsHome.as_view(), name='shop'),
    path('city/<slug:city_slug>', city_slug, name='city_slug'),
    path('contacts/', contacts, name='contacts'),
    path('jobs/', jobs, name='jobs'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),
    path('product/<slug:post_slug>/', ShowProduct.as_view(), name='product'),
    path('webhook/', csrf_exempt(my_webhook_handler))
]
