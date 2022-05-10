from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from snowpenguin.django.recaptcha2.fields import ReCaptchaField
# from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from .models import UploadFile, FeedFile
from django.forms import ClearableFileInput

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']





class UploadForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_semestr = forms.IntegerField(label='Семестр', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_course = forms.IntegerField(label='Курс', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UploadFile
        fields = ('number_course','number_semestr','title', 'description','price')

class FileModelForm(forms.ModelForm):
    class Meta:
        model = FeedFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class FileFilterForm(forms.Form):
    number_course = forms.IntegerField(label='Курс',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_semestr = forms.IntegerField(label='Семестр',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subjectt = forms.CharField(label='Дисциплина',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    type_materials = forms.CharField(label='Тип работы',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())