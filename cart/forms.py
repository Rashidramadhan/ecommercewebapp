from django import forms


from .models import CartItemsModel

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartItemsForm(forms.ModelForm):
    class Meta:
        model = CartItemsModel
        fields = '__all__'
