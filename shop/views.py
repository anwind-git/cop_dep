import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from .utils import *
from recipes.models import *
from django.db.models import Sum
from django.db.models.functions import Round
from django.shortcuts import render, redirect
from orders.tasks import payment_search
from yookassa import Payment


class BaseClassProduct(DataMixin, ListView):
    model = Products
    template_name = 'shop/index.html'
    context_object_name = 'products'


class ProductsHome(BaseClassProduct):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Магазин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True).exclude(id__in=self.get_cart())


class ProductsCategory(BaseClassProduct):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Категория - {str(MenuCategories.objects.get(slug=self.kwargs["cat_slug"]))}',
                                      cat_selected=self.kwargs['cat_slug'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(menu_categories__slug=self.kwargs['cat_slug'],
                                       cities=city_id, publication=True).exclude(id__in=self.get_cart())


class ShowProduct(DataMixin, DetailView):
    model = Products
    template_name = 'shop/product.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['ingredients'] = AddIngredientToRecipe.objects.filter(recipe=obj.id).prefetch_related('ingredient')
        context['kjby'] = AddIngredientToRecipe.objects.filter(recipe=obj.id).aggregate(
            withs=Sum(obj.recipe.serving_weight) / Count(obj.recipe.serving_weight),
            kcal=Round(Sum('kcal') * obj.recipe.serving_weight / Sum('weight'), 2),
            fats=Round(Sum('fats') * obj.recipe.serving_weight / Sum('weight'), 2),
            squirrels=Round(Sum('squirrels') * obj.recipe.serving_weight / Sum('weight'), 2),
            carbs=Round(Sum('carbs') * obj.recipe.serving_weight / Sum('weight'), 2)
        )

        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_context = self.get_user_context()
        city_id = user_context['city']['city_id']
        return Products.objects.filter(cities=city_id, publication=True)


def city_slug(request, city_slug):
    request.session.pop('cart', None)
    city = Cities.objects.get(slug=city_slug)
    values = {'city_id': city.id, 'city_name': city.city, 'city_slug': city.slug}
    request.session['city'] = values
    return redirect('shop:shop')


def jobs(request):
    return render(request, 'shop/jobs.html', {'menu': menu, 'title': 'Вакансии'})


def contacts(request):
    return render(request, 'shop/contacts.html', {'menu': menu, 'title': 'Контакты'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@csrf_exempt
def my_webhook_handler(request):
    try:
        event_json = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponse(status=400)
    notification_object = WebhookNotification(event_json)
    payment = notification_object.object
    payment_log = Payment.find_one(payment.id)
    if payment_log.status == 'succeeded':
        payment_search.delay(payment.id)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


