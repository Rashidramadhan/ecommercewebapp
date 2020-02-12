from django.db import models



# Create your models here.


class OrderModel(models.Model):
    order_id = models.CharField(max_length=60)
    item = models.CharField(max_length=100, null=False, blank=True)
    username = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=False)



    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # amount = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order{}'.format(self.order_id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class SalesModel(models.Model):
    # order_id = models.ForeignKey(OrderModel, related_name='orders', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    payment_option = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.id)

    # def get_cost(self):
    #     return self.price * self.quantity


class DeliveryDetailsModel(models.Model):
    username = models.CharField(max_length=60, null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    # email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

