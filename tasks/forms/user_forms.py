from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from tasks.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """
    Mirrors Django's stock UserCreationForm but targets our CustomUser model
    and adds extra server-side rules.
    """
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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
    
    def clean_password1(self):
        """
        Validates the password field against Django's password validators in settings.py.
        """
        password = self.cleaned_data.get("password1")
        if password:
            # We need a user object for the UserAttributeSimilarityValidator.
            # Since the user isn't saved yet, we create a temporary instance
            # and populate it with the other form data.
            user_instance = self.instance # Gets an unsaved CustomUser object
            user_instance.first_name = self.cleaned_data.get('first_name', '')
            user_instance.last_name = self.cleaned_data.get('last_name', '')
            user_instance.email = self.cleaned_data.get('email', '')
            
            try:
                validate_password(password, user=user_instance)
            except ValidationError as error:
                # The validate_password helper raises a ValidationError.
                # We add it to the password1 field's errors.
                self.add_error('password1', error)
                
        return password

    def clean(self):
        """
        This method still runs after all the individual clean_field methods.
        It's still the perfect place to check that the two passwords match.
        """
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
