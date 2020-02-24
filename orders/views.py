from __future__ import print_function
import traceback
import sys
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from .models import *

# Create your views here.


def index(request):
    return render(request, "orders/index.html")


# Create your views here.
def menu(request):
    return render(request, "orders/menu.html")


def services(request):
    return render(request, "orders/services.html")


def menu(request):
    context = {
        "pizzas": PizzaName.objects.all(),
        "subs": SubName.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": DinnerPlatterName.objects.all(),
        "toppings": Topping.objects.all(),
        "sizes": Size.objects.all()}
    return render(request, "orders/pizzas.html", context=context)


class ShoppingListView(ListView):
    model = Pizza
    template_name = 'orders/shopping-cart.html'  # <app>/<model>_<viewtype>.html
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@csrf_exempt
def order(request):
    if request.method == 'GET':
        return

    elif request.method == 'POST':
        print(json.loads(request.body))

        type = json.loads(request.body)["type"]
        product = json.loads(request.body)["product"]
        quantity = json.loads(request.body)["quantity"]
        print(type)
        order = Order.objects.filter(
            user__pk=request.user.id).filter(order_sent=False)

        if order.count() == 0:
            order = Order(user=request.user)
            order.save()

        else:

            order = order[0]

        if (type == "pizza"):
            print(json.loads(request.body))
            size = json.loads(request.body)["size"]
            amount = json.loads(request.body)["amount"]
            topping = json.loads(request.body)["topping"]
            order_pizza = OrderPizza(
                order=order,
                pizza=Pizza.objects.create(
                    name=PizzaName.objects.get(name=product),
                    size=Size.objects.get(name=size),
                    toppings_count=int(1)
                ),
                quantity=1
            )
            order_pizza.save()
            for topping_name in topping:
                order_pizza.toppings.add(
                    Topping.objects.get(name=topping_name)
                )

            order_pizza.save()

        elif type == "subs":
            size = json.loads(request.body)["size"]
            order_sub = OrderSub(
                order=order,
                sub=Sub.objects.get(
                    name=SubName.objects.get(name=product),
                    size=Size.objects.get(name=size)
                ),
                quantity=quantity
            )
            order_sub.save()

            order.save()
        elif type == "salads":
            order_salad = OrderSalad(
                order=order,
                salad=Salad.objects.get(
                    name=Salad.objects.get(name=product)
                ),
                quantity=quantity
            )
            order_salad.save()
            order.save()
        elif type == "pastas":
            order_pasta = OrderPasta(
                order=order,
                pasta=Pasta.objects.get(
                    name=Pasta.objects.get(name=product)
                ),
                quantity=quantity
            )
            order_pasta.save()
            order.save()
        elif type == "dinnerPlatters":
            size = json.loads(request.body)["size"]
            order_dinner_platter = OrderDinnerPlatter(
                order=order,
                dinner_platter=DinnerPlatter.objects.get(
                    name=DinnerPlatterName.objects.get(name=product),
                    size=Size.objects.get(name=size)
                ),
                quantity=quantity
            )
            order_dinner_platter.save()
            order.save()

        # order_pizza.save()

        # Add to order

        if request.is_ajax():
            message = "Success"
            # order = Order.objects.create(
            # user=request.user, pizza=pizza, price=price)

            return HttpResponse(message)
        else:
            message = "Not Ajax"
            return HttpResponse(message)


def cart(request, order_id=None):
    context = {
        "order_exists": False
    }

    if order_id is None:
        order = Order.objects.filter(
            user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            return render(request, "orders/shopping-cart.html", context=context)
        else:
            order = order[0]
    else:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotFound:
            return render(request, "orders/shopping-cart.html", context=context)

    context["order_exists"] = True
    context.update({
        "pizzas": OrderPizza.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "subs": OrderSub.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "pastas": OrderPasta.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "salads": OrderSalad.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "dinner_platters": OrderDinnerPlatter.objects.filter(
            order=Order.objects.get(pk=order.id)
        ),
        "overall_price": order.get_order_price(),
        "order_id": order.id
    })

    if order_id is None:
        context["order_title"] = "Your current order"
        context["buttons"] = True
    else:
        context["order_title"] = f"Order #{order_id}"
        context["buttons"] = False

    print(context)
    return render(request, "orders/shopping-cart.html", context=context)


@csrf_exempt
def remove_from_cart(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    print(request)

    order_class = json.loads(request.body)["model"]
    order_id = json.loads(request.body)["id"]

    order = Order.objects.filter(
        user__pk=request.user.id).filter(order_sent=False)[0]

    class_obj = globals()[order_class]
    order_product = class_obj.objects.get(pk=order_id)
    order_product.delete(keep_parents=True)

    return JsonResponse({
        "order_price": order.get_order_price()
    })


@csrf_exempt
def confirm_order_final(request):
    if request.method == "POST":
        order = Order.objects.filter(
            user__pk=request.user.id).filter(order_sent=False)
        if order.count() == 0:
            return HttpResponseNotFound()
        else:
            order = order[0]

        order.order_sent = True
        order.save()

        return JsonResponse({"success": True}, safe=False)
    else:
        return HttpResponseNotAllowed()


@csrf_exempt
def cancel_order(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()

    order = Order.objects.filter(
        user__pk=request.user.id).filter(order_sent=False)
    if order.count() == 0:
        return HttpResponseNotFound()
    else:
        order = order[0]

    order.delete(keep_parents=True)

    return JsonResponse({"success": True}, safe=False)


class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        # Just print the exception object to stdout
        print(exception)

        # Print the familiar Python-style traceback to stderr
        traceback.print_exc()

        # Write the traceback to a file or similar
        myfile.write(''.join(traceback.format_exception(*sys.exc_info())))


@login_required
def orders_history(request):
    context = {
        "orders": []
    }

    orders = Order.objects.filter(user__pk=request.user.id).filter(
        order_sent=True).order_by("-created")
    context["orders"] = orders

    return render(request, "orders/orders_history.html", context=context)
