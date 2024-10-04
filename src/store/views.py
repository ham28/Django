# store/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}

    # Vérifiez si l'utilisateur est authentifié
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # Gestion des sessions pour les utilisateurs non authentifiés
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            orderItem = {'product': product, 'quantity': quantity}
            items.append(orderItem)
            order['get_cart_items'] += quantity
            order['get_cart_total'] += product.price * quantity

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # Gestion des sessions pour les utilisateurs non authentifiés
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            orderItem = {'product': product, 'quantity': quantity}
            items.append(orderItem)
            order['get_cart_items'] += quantity
            order['get_cart_total'] += product.price * quantity

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
    else:
        # Gestion du panier pour les utilisateurs non authentifiés
        cart = request.session.get('cart', {})

        if action == 'add':
            if productId in cart:
                cart[productId] += 1
            else:
                cart[productId] = 1
        elif action == 'remove':
            if productId in cart:
                cart[productId] -= 1
                if cart[productId] <= 0:
                    del cart[productId]

        request.session['cart'] = cart

    return JsonResponse('Item was added', safe=False)
