from django import forms

class BromoCodeForm(forms.Form):
    code = forms.CharField(max_length=20,)
    def clean(self):
        cleaned_data = super(BromoCodeForm, self).clean()
        return cleaned_data
        


class CommentForm(forms.Form):
    comment = forms.Textarea()
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data

