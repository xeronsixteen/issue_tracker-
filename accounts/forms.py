from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django.contrib.auth import login, get_user_model
from django import forms

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    email = EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    # def clean_email(self):
    #     email = self.cleaned_data['email'].strip()
    #     if User.objects.filter(email__iexact=email).exists():
    #         raise ValidationError('Такое мыло существует в БД')
    #     return email
    #
    # def clean_username(self):
    #     username = self.cleaned_data['username'].strip()
    #     if User.objects.filter(username__iexact=username).exists():
    #         raise ValidationError('Такое имя существует в БД')
    #     return username
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data['first_name'].strip()
    #     last_name = cleaned_data['last_name'].strip()
    #     if not first_name and not last_name:
    #         raise ValidationError('Заполните хотя бы одно из полей : имя или фамилия')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'git', 'bio']
