from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils import timezone

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
        widget=forms.FileInput(attrs={"class": "form-control"})
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
        print(profile.avatar)
        profile.set_password(self.cleaned_data["password"])

        if commit:
            profile.save()

        return profile
