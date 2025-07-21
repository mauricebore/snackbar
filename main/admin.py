from django.contrib import admin
from .models import MenuItem
from .models import Order, OrderItem

admin.site.register(MenuItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('customer_name',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item_name', 'price', 'quantity')
    search_fields = ('item_name',)



# Register your models here.
