from django import forms
from django.contrib.auth import password_validation
from django.core import validators
from django.contrib.auth.password_validation import *
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150,required=True,label='Username')
    first_name = forms.CharField(max_length=150,label='Firstname')
    last_name = forms.CharField(max_length=150,label='Lasttname')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                help_text=password_validation,
                                )
    repassword = forms.CharField(label='Re-Password',widget = forms.PasswordInput)

    """ def cleaned_data(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('repassword'):
            raise forms.ValidationError('Password are not equal')
        return self.cleaned_data

        def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        ) """

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password','repassword']

class ChangePasswordForm(forms.ModelForm):
    oldpassword = forms.CharField(label='Old-Password',widget=forms.PasswordInput,)
    newpassword = forms.CharField(label='New-Password',
                                widget=forms.PasswordInput,
                                help_text=password_validation,
                                validators=[MinimumLengthValidator])
    renewpassword = forms.CharField(label='Re-New-Password',widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['oldpassword','newpassword','renewpassword']

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150,label='Firstname')
    last_name = forms.CharField(max_length=150,label='Lasttname')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['first_name','last_name','email']