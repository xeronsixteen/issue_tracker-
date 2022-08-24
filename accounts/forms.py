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


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']
