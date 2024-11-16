from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from accounts.models import User

class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha",
            }
        )
    )


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Crie uma senha",
            }
        ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme sua senha",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu email",
                }
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
