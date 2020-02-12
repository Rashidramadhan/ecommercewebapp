from django import forms
from .models import OrderModel, DeliveryDetailsModel, SalesModel



class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['item']


class SalesForm(forms.ModelForm):
    class Meta:
        model = SalesModel
        fields = ['payment_option', 'total_amount']


# class PurchaseForm(forms.Form):
#
#     total_amount = forms.DecimalField(decimal_places=2)
#     items = forms.TextInput()
#     payment_option = forms.CharField(max_length=20, required=True)


class DeliveryDetailsForm(forms.ModelForm):
    class Meta:
        model = DeliveryDetailsModel
        fields = ['first_name', 'last_name', 'phone_number', 'address']
