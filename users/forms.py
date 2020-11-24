from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

Profile = get_user_model()


class DateInputCalendar(forms.DateInput):
    input_type = "date"


class LoginForm(auth_forms.AuthenticationForm):
    """
    Add label and styles to default authentication form
    """
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'autocomplete': "off"})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'autocomplete': "off"})
    )


class ProfileForm(forms.ModelForm):
    TODAY = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')

    birthdate = forms.DateField(
        required=False,
        label="Дата рождения", widget=DateInputCalendar(attrs={
            "class": "form-control",
            "max": f"{TODAY}"
        })
    )
    avatar = forms.FileField(
        required=False, label="Аватар",
        widget=forms.FileInput(attrs={"class": "custom-file-input"})
    )
    first_name = forms.CharField(
        required=False, label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False, label="Фамилия",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        required=False, label="E-mail",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    info = forms.CharField(
        required=False, label="О себе",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = Profile
        fields = ("avatar", "first_name",
                  "last_name", "email",
                  "birthdate", "info",)


class ProfileRegisterForm(ProfileForm):
    username = forms.CharField(
        required=True, label="Имя пользователя*",
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'autocomplete': "off"})
    )
    password = forms.CharField(
        required=True, label="Пароль*",
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          'autocomplete': "off"})
    )

    class Meta:
        model = Profile
        fields = ("username", "password",
                  "avatar", "first_name",
                  "last_name", "email",
                  "birthdate", "info",)

    def save(self, commit=True):
        profile = super(ProfileRegisterForm, self).save(commit=False)
        profile.set_password(self.cleaned_data["password"])

        if commit:
            profile.save()

        return profile


class ProfileChangePasswordForm(forms.ModelForm):
    """
    Add label and styles to default PasswordChangeForm form
    """
    old_password = forms.CharField(
        label=_('Текущий пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_('Новый пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label=_('Подтвердите новый пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ("old_password", "new_password1", "new_password2")

    def clean(self):
        cleaned_data = super(ProfileChangePasswordForm, self).clean()
        new_password1 = cleaned_data["new_password1"]
        new_password2 = cleaned_data["new_password2"]
        old_password = cleaned_data["old_password"]
        if new_password1 != new_password2:
            self.add_error("new_password1", _("Пароли не совпадают"))
        if new_password1 == old_password:
            self.add_error("new_password1", _("Пароль не может дублирывать старый пароль"))
        if not self.instance.check_password(old_password):
            self.add_error("old_password", _("Пароль не верный"))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ProfileChangePasswordForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super(ProfileChangePasswordForm, self).save(commit=False)
        profile.set_password(self.cleaned_data["new_password1"])

        if commit:
            profile.save()

        return profile
