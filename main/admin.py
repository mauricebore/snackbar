from django.contrib import admin
from django.utils.html import format_html
from .models import MenuItem, Order, OrderItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'stock_status_coloured')

    def stock_status_coloured(self, obj):
        if obj.quantity == 0:
            color = 'red'
            status = 'Out of Stock'
        elif obj.quantity < 5:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'green'
            status = 'In Stock'

        return format_html('<span style="color: {};">{}</span>', color, status)

    stock_status_coloured.short_description = 'Stock Status'

admin.site.register(MenuItem, MenuItemAdmin)


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
