from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# ModelForm: form được tạo từ model, tạo những ô input y như bên model
# Form: dạng custom form

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
            raise ValidationError(f'Username đã tồn tại!')
        except User.DoesNotExist:
            return username
            
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
            raise ValidationError(f'Email đã tồn tại!')
        except User.DoesNotExist:
            return email

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise ValidationError(f'Mật khẩu nhập lại không giống nhau!')
        return self.cleaned_data['confirm_password']
    
    def save(self):
        User.objects.create_user(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            email = self.cleaned_data['email'],
        )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Tên đăng nhập', widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=30, label='Mật khẩu', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
