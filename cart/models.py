from django.db import models

# Create your models here.


class CartItemsModel(models.Model):
    product = models.TextField(max_length=100)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.TextField()

