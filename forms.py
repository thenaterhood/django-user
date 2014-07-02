from django import forms  # bring in the forms framework
# needed to fill in User information records and save them
from django.contrib.auth.models import User
# used so we can inherit this in our new class
from django.contrib.auth.forms import UserCreationForm
import re
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(UserCreationForm):

    """
    Defines the first part of the user registration form.
    """
    email = forms.EmailField(required=True, widget=forms.TextInput(),
                             help_text="Used for some notifications and to retrieve your profile from Gravatar. Never displayed publicly.")  # creates an email field that is required
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "max_length": 30, "placeholder": "First Name", "class": "form-control"}), label=(""))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "max_length": 30, "placeholder": "Last Name", "class": "form-control"}), label=(""))
    username = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "max_length": 10, "placeholder": "Username", "class": "form-control"}), label=(""))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"required": True, "max_length": 30, "placeholder": "Email", "class": "form-control"}), label=(""))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"required": False, "render_value": False, "placeholder": "Password", "class": "form-control"}), label=(""))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"required": False, "render_value": False, "placeholder": "Confirm Password", "class": "form-control"}), label=(""))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        """
        Saves the information included in the above form

        Returns:
                user - An updated/saved django user instance
        """

        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username'].lower()
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class EditUserForm(forms.ModelForm):

    email = forms.EmailField(help_text="Used for some notifications and to retrieve your profile from Gravatar. Never displayed publicly.", widget=forms.TextInput(
        attrs={"required": True, "placeholder": "Email Address", "class": "form-control"}), label=(""))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "placeholder": "First Name", "class": "form-control"}), label=(""))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "placeholder": "Last Name", "class": "form-control"}), label=(""))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class PasswordForm(forms.Form):

    password0 = forms.CharField(widget=forms.PasswordInput(
        attrs={"required": False, "render_value": False, "placeholder": "Current Password", "class": "form-control"}), label=(""))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"required": False, "render_value": False, "placeholder": "New Password", "class": "form-control"}), label=(""))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"required": False, "render_value": False, "placeholder": "Confirm New Password", "class": "form-control"}), label=(""))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _("The two password fields did not match."))
        return self.cleaned_data


class AddMemberForm(forms.Form):

    """
    Defines a form for entering a username of a site 
    member.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "max_length": 50, "placeholder": "Add Member", 'class': 'form-control'}), label=(""))

    class Meta:
        fields = ('username')
