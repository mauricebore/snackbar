from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('biscuits', 'Biscuits'),
        ('drinks', 'Drinks'),
        # Add more categories if needed
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/menu_images/')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='drinks')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"


image = models.ImageField(upload_to='media/menu_images/', blank=True, null=True)



# Create your models here.
