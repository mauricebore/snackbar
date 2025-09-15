from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from .forms import MenuItemForm
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F, FloatField
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.shortcuts import render
from .models import MenuItem

def home(request):
    biscuits = MenuItem.objects.filter(category='biscuits')
    drinks = MenuItem.objects.filter(category='drinks')
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    
    return render(request, 'main/home.html', {
        'biscuits': biscuits,
        'drinks': drinks,
        'cart_count': cart_count
    })


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


def is_admin_user(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = MenuItem.objects.count()
    low_stock_items = MenuItem.objects.filter(quantity__lt=5)
    recent_orders = Order.objects.order_by('-created_at')[:10]

    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'low_stock_items': low_stock_items,
        'recent_orders': recent_orders,
    }

    return render(request, 'main/admin_dashboard.html', context)

    


def add_product(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'main/add_product.html', {'form': form})


def product_list(request):
    products = MenuItem.objects.all()
    return render(request, 'main/product_list.html', {'products': products})




def update_product(request, pk):
    product = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.save()
    return redirect('product_list')


def edit_product(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'main/edit_product.html', {'form': form, 'item': item})



def delete_product(request, pk):
    product = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('product_list')


def add_product(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'main/add_product.html', {'form': form})





def restock_product(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        item.quantity += amount
        item.save()
        return redirect('admin_dashboard')
    return render(request, 'main/restock_product.html', {'item': item})


def user_list(request):
    users = User.objects.all()
    return render(request, 'main/user_list.html', {'users': users})

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_list')
    return render(request, 'main/edit_user.html', {'user': user})

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted.')
    return redirect('user_list')

def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'User {"activated" if user.is_active else "deactivated"}.')
    return redirect('user_list')



# Create your views here.
