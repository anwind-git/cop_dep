from decimal import Decimal
from django.shortcuts import redirect
from django.views.generic import TemplateView


from .models import OrderItem, Orders
from cart.cart import Cart
from shop.utils import *
from dadata import Dadata
from yookassa import Configuration, Payment
import uuid

#ключи подсказки адрес, почта, телефон
token = ""
secret = ""
dadata = Dadata(token, secret)

#ключи юкасса
Configuration.account_id = ''
Configuration.secret_key = ''


class YooMoneyCheckoutWidget(DataMixin, TemplateView):
    template_name = 'orders/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказа')
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request):
        cart = Cart(request)
        if request.method == 'POST':
            try:
                last_object = Orders.objects.latest('id')
                last_id = last_object.id
                next_id = last_id + 1
            except Orders.DoesNotExist:
                next_id = 1
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)

                items_list = []
                for i in cart:
                    items = {
                        "description": i['product'],
                        "quantity": i['quantity'],
                        "amount": {
                            "value": i['price'],
                             "currency": "RUB"
                        },
                        "vat_code": "4", #Код ставки НДС 20%
                        "payment_mode": "full_prepayment", # Признак способа расчета полная предоплата
                        "payment_subject": "commodity", # Признак предмета расчета товар
                        "country_of_origin_code": "RU", # код страны происхождения
                        "mark_mode": 0,
                        "mark_code_info":
                        {
                            "gs_1m": "DFGwNDY0MDE1Mzg2NDQ5MjIxNW9vY2tOelDFuUFwJh05MUVFMDYdOTJXK2ZaMy9uTjMvcVdHYzBjSVR3NFNOMWg1U2ZLV0dRMWhHL0UrZi8ydkDvPQ=="
                        },
                            "measure": "piece"
                        }
                    items_list.append(items)
                total_cost = Decimal(cart.get_total_price()) * Decimal(1 + 3.7/100)
                idempotence_key = str(uuid.uuid4())
                response = Payment.create({
                    "amount": {
                        "value": total_cost,
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": f"https://{self.request.get_host()}"
                    },
                    "capture": True,
                    "description": f"Заказ №{next_id}",
                    "metadata": {
                        'orderNumber': next_id
                    },
                    "receipt": {
                        "customer": {
                            "email": self.request.POST.get("email")
                        },
                        "items": items_list
                    },
                    "payment_method_data": {
                        "type": "bank_card"
                    },


                }, idempotence_key)

                order.identifier = response.id
                order.phone = self.request.POST.get("phone")
                order.city = Cities.objects.get(id=self.get_user_context()['city']['city_id'])
                order.save()

                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                cart.clear()
                return redirect(response.confirmation.confirmation_url)

