from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class DistributorLoginForm(AuthenticationForm):
    username = forms.CharField(label="Distributor Name",widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Distributor Name',
            'autocomplete':'off',
            
    }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your Distributor ID is your password',
            'autocomplete':'off',
    }
    ))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username is not None and password is not None:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return cleaned_data
