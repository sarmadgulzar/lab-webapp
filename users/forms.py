from allauth.account.forms import LoginForm, SignupForm
from django import forms


class LabLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LabLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "aria-describedby": "login-input-validation",
            }
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "aria-describedby": "password-input-validation",
            }
        )


class LabSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(LabSignUpForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "aria-describedby": "email-input-validation",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "aria-describedby": "password1-input-validation",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "aria-describedby": "password2-input-validation",
            }
        )
