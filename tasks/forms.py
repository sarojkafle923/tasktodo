from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    Mirrors Django's stock UserCreationForm but targets our CustomUser model
    and adds extra server-side rules.
    """
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "minlength": 8}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "minlength": 8}),
        strip=False
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")

    # ----------  BACK-END VALIDATION ----------
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that e-mail already exists.")
        return email

    def clean(self):
        super().clean()
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords do not match.")
        # Add any bespoke cross-field rules here
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
