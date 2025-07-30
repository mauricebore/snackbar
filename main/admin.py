from django.contrib import admin
from django.utils.html import format_html
from .models import MenuItem, Order, OrderItem

# Customize Admin Site Titles
admin.site.site_header = "Snack Bar Admin"
admin.site.site_title = "Snack Bar Admin Portal"
admin.site.index_title = "Welcome to the Snack Bar Admin Dashboard"

# MenuItem Admin
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'stock_status_coloured')
    list_filter = ('category',)
    search_fields = ('name',)

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

# Inline OrderItem for OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_name', 'price', 'quantity')

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('customer_name',)
    inlines = [OrderItemInline]

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item_name', 'price', 'quantity')
    search_fields = ('item_name',)


# Register your models here.
