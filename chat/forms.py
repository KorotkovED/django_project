from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from snowpenguin.django.recaptcha2.fields import ReCaptchaField
# from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from .models import UploadFile, FeedFile, Writehelp, WhiteHelpFile
from django.forms import ClearableFileInput
from django.contrib.admin.widgets import AdminSplitDateTime, AdminDateWidget, AdminTimeWidget

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
    number_semestr = forms.IntegerField(label='Семестр', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_course = forms.IntegerField(label='Курс', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subjectt = forms.CharField(label='Дисциплина', required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    type_materials = forms.CharField(label='Тип материала', required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    institute = forms.CharField(label='Институт', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UploadFile
        fields = ('number_course','number_semestr','type_materials','institute','subjectt','title','description','price')

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
    type_materials = forms.CharField(label='Тип материала',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    institute = forms.CharField(label='Институт',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())

class WritehelpForm(forms.ModelForm):
    titles = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    descriptions = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-control'}))
    semestr = forms.IntegerField(label='Семестр', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    course = forms.IntegerField(label='Курс', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subjects = forms.CharField(label='Дисциплина', required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    prices = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    institutes = forms.CharField(label='Институт', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # createdtimes = forms.DateField(label='Создан')
    # time = forms.TimeField(label='Время',widget= AdminTimeWidget())
    date = forms.DateField(label='Дата',widget= AdminDateWidget())


    class Meta:
        model = Writehelp
        fields = ('course','semestr','institutes','subjects','titles','descriptions','prices','date')
        # widgets = {
        #     # 'time': AdminTimeWidget(),
        #     'date': AdminDateWidget()
        # }
class WhiteHelpFileForm(forms.ModelForm):
    class Meta:
        model = WhiteHelpFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

# class FileFilterForm(forms.Form):
#
#     number_course = forms.IntegerField(label='Курс',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     number_semestr = forms.IntegerField(label='Семестр',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     subjectt = forms.CharField(label='Дисциплина',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
#     type_materials = forms.CharField(label='Тип материала',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
#     institute = forms.CharField(label='Институт',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))