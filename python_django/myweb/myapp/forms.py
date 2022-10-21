from django import forms
from django.core.exceptions import ValidationError
from .models import Pet
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

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__' # chọn hết
        #field = ('name','age','type') chọn cái hiển thị
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'vacinated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dewormed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sterilized': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('id', None)
            self.fields.pop('name', None)
    
    # Khi tạo server validate thì tạo ở forms
    # Khi muốn validate cho 1 field thì tại hàm có dạng clean_<tên field>
    def clean_id(self):
        print('Validate id')
        # thử lấy pet với id người dùng gửi lên
        # nếu trả về 1 pet object thì id đã trùng
        # nếu không trả về id thì trả lại id, tiếp tục xử lý
        try:
            Pet.objects.get(id=self.cleaned_data['id'])
            pet_id = self.cleaned_data['id']
            print('Trùng id pet!')
            raise ValidationError(f'Pet với id: {pet_id} đã tồn tại!')
        except Pet.DoesNotExist:
            print('Id pet ok!')
            return self.cleaned_data['id']
    
    def clean_name(self):
        print('Validate name')
        # thử lấy pet với id người dùng gửi lên
        # nếu trả về 1 pet object thì id đã trùng
        # nếu không trả về id thì trả lại id, tiếp tục xử lý
        try:
            Pet.objects.get(name=self.cleaned_data['name'])
            pet_name = self.cleaned_data['name']
            print("Trùng tên!")
            raise ValidationError(f'Pet với tên: {pet_name} đã tồn tại!')
        except Pet.DoesNotExist:
            print("không trùng tên!")
            return self.cleaned_data['name']