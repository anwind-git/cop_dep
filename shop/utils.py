from .models import *
from django.db.models import *
from django.shortcuts import get_object_or_404
from organizations.models import Cities
from django.core.cache import cache
from cart.forms import CartAddProductForm
from orders.forms import OrderCreateForm

menu = [{'title': 'Магазин', 'url_name': '.'},
        {'title': 'Вакансии', 'url_name': 'jobs'},
        {'title': 'Контакты', 'url_name': 'contacts'}
        ]


class DataMixin:
    paginate_by = 9

    def get_cart(self):
        product_ids_in_cart = map(str, self.request.session.get('cart', {}).keys())
        return product_ids_in_cart

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = MenuCategories.objects.annotate(Count('products'))
        if 'city' not in self.request.session:
            first_city = Cities.objects.first()
            values = {'city_id': first_city.id, 'city_name': first_city.city}
            self.request.session['city'] = values
        context['city'] = self.request.session['city']
        context['cart_product_form'] = CartAddProductForm
        context['menu'] = menu
        context['categories'] = categories
        context['cities'] = Cities.objects.all()
        context['form'] = OrderCreateForm
        if 'cat_select' not in context:
            context['cat_select'] = 0
        return context



