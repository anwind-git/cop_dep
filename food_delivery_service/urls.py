from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from shop.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls', namespace='orders')),
    path('', include('shop.urls')),
    path('shop', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('webhook/', csrf_exempt(my_webhook_handler))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        # ...
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = pageNotFound
