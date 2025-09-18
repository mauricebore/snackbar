# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    
    # Cart functionality
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    # Admin pages
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('order-history/', views.order_history, name='order_history'),
    
    # Product management
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('restock-product/<int:pk>/', views.restock_product, name='restock_product'),
    
    # User management
    path('users/', views.user_list, name='user_list'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('toggle-user-active/<int:pk>/', views.toggle_user_active, name='toggle_user_active'),
]