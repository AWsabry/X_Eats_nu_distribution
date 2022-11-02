from django import forms

class QuantityForm(forms.Form):
    Quantity = forms.IntegerField(min_value=1,initial=1)
    def clean(self):
        cleaned_data = super(QuantityForm, self).clean()
        return cleaned_data


class Order_time(forms.Form):
    timing = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(Order_time, self).clean()
        return cleaned_data
        