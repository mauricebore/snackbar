"""snackbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('orders/', views.order_history, name='order_history'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin-panel/add-product/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('admin-panel/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin-panel/restock-product/<int:pk>/', views.restock_product, name='restock_product'),
    path('admin-panel/update-product/<int:pk>/', views.update_product, name='update_product'),
    path('admin-panel/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin-panel/users/', views.user_list, name='user_list'),
    path('admin-panel/users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('admin-panel/users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('admin-panel/users/toggle/<int:pk>/', views.toggle_user_active, name='toggle_user_active'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


