from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F, FloatField
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta

def home(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render(request, 'main/home.html', {'cart_count': cart_count})

def menu(request):
    biscuits = MenuItem.objects.filter(category='biscuits')
    drinks = MenuItem.objects.filter(category='drinks')
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    
    context = {
        'biscuits': biscuits,
        'drinks': drinks,
        'cart_count': cart_count
    }
    
    return render(request, 'main/menu.html', context)


def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    current_quantity_in_cart = cart.get(str(item_id), {}).get('quantity', 0)

    if current_quantity_in_cart < item.quantity:
        if str(item_id) in cart:
            cart[str(item_id)]['quantity'] += 1
        else:
            cart[str(item_id)] = {
                'name': item.name,
                'price': float(item.price),
                'quantity': 1,
                'image': item.image.url if item.image else '',
            }
        messages.success(request, f"{item.name} added to cart.")
    else:
        messages.error(request, f"Cannot add more {item.name}. Only {item.quantity} available.")

    request.session['cart'] = cart
    return redirect('menu')


def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'main/cart.html', {'cart': cart, 'total': total})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        if not customer_name:
            messages.error(request, "Please enter your name.")
            return redirect('checkout')

        try:
            with transaction.atomic():  # Begin atomic transaction
                for id, item in cart.items():
                    menu_item = MenuItem.objects.select_for_update().get(id=id)
                    if menu_item.quantity < item['quantity']:
                        messages.error(request, f"Sorry! Only {menu_item.quantity} of {menu_item.name} left.")
                        return redirect('menu')

                order = Order.objects.create(customer_name=customer_name)

                for id, item in cart.items():
                    menu_item = MenuItem.objects.get(id=id)
                    OrderItem.objects.create(
                        order=order,
                        item_name=item['name'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    menu_item.quantity = F('quantity') - item['quantity']
                    menu_item.save()

            request.session['cart'] = {}
            messages.success(request, f"Order placed successfully for {customer_name}.")
            return render(request, 'main/checkout_success.html', {'order': order})

        except MenuItem.DoesNotExist:
            messages.error(request, "One of the items no longer exists.")
            return redirect('menu')

    else:
        total = sum(item['price'] * item['quantity'] for item in cart.values())
        return render(request, 'main/checkout.html', {'cart': cart, 'total': total})


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        if cart[str(item_id)]['quantity'] > 1:
            cart[str(item_id)]['quantity'] -= 1
        else:
            del cart[str(item_id)]
    
    request.session['cart'] = cart
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')


@staff_member_required
@login_required
def order_history(request):
    filter_option = request.GET.get('filter', 'all')
    orders = Order.objects.prefetch_related('items').annotate(
        total=Sum(F('items__price') * F('items__quantity'), output_field=FloatField())
    ).order_by('-created_at')

    today = timezone.now().date()

    if filter_option == 'today':
        orders = orders.filter(created_at__date=today)
    elif filter_option == 'week':
        start_week = today - timedelta(days=today.weekday())
        orders = orders.filter(created_at__date__gte=start_week)
    elif filter_option == 'month':
        orders = orders.filter(created_at__month=today.month, created_at__year=today.year)

    # Calculate grand total of all filtered orders
    grand_total = sum(order.total or 0 for order in orders)

    return render(request, 'main/order_history.html', {
        'orders': orders,
        'filter': filter_option,
        'grand_total': grand_total,
    })




# Create your views here.
