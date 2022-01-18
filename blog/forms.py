from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .apps import user_registered
from .models import User, Training


# class UserForm(forms.ModelForm):
#     mail_adr = forms.EmailField(required=True, label='Эл.почта')
#
#     class Meta:
#         model = User
#         fields = ('phone_number', 'first_name', 'second_name', 'mail_adr')


class ChangeUserInfoForm(forms.ModelForm):
    mail_adr = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'mail_adr')


class RegisterUserForm(forms.ModelForm):
    mail_adr = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают',
                                                   code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'mail_adr')


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
        # widgets = {'author': forms.HiddenInput}


# AIFormSet = inlineformset_factory(Training, fields='__all__')


