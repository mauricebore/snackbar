from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from django.contrib import messages

def home(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'main/home.html', {'cart_count': cart_count})

def menu(request):
    items = MenuItem.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'main/menu.html', {'items': items, 'cart_count': cart_count})

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name': item.name,
            'price': float(item.price),
            'quantity': 1,
            'image': item.image,
        }

    request.session['cart'] = cart

    messages.success(request, f"{item.name} added to cart.")
    
    return redirect('menu')

def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'main/cart.html', {'cart': cart, 'total': total})

def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('view_cart')

        # For simplicity, use a placeholder customer name or collect it via form later
        order = Order.objects.create(customer_name="Walk-in Customer")

        for id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                item_name=item['name'],
                price=item['price'],
                quantity=item['quantity']
            )
        # Clear cart after checkout
        request.session['cart'] = {}
        return render(request, 'main/checkout_success.html', {'order': order})
    else:
        return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        if cart[str(item_id)]['quantity'] > 1:
            cart[str(item_id)]['quantity'] -= 1
        else:
            del cart[str(item_id)]
    
    request.session['cart'] = cart
    return redirect('view_cart')


# Create your views here.
