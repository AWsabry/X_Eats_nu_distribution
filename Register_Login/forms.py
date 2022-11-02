from django import forms
from Register_Login.models import Events, Profile, Restaurant_Suggestion
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate



class RegisterForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'password1','password2','title', 'PhoneNumber','nu_id','school')
        error_messages = {
            'email': {
                'unique': _("This entry has been registered before."),
            }
        }
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class LoginForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email = email, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Password is incorrect")
        if not user.is_active:
            raise forms.ValidationError("This user is not active, check Your inbox or make sure you logged in with valid email")
        return super(LoginForm,self).clean(*args,**kwargs)


class Restaurant_suggestion(forms.ModelForm):
    class Meta:
        model = Restaurant_Suggestion
        fields = ('email','city','restaurant_name','reason')


class Event_form(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('email','first_name','last_name','PhoneNumber','Organization','date','Quantity')





