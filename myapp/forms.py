from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

INPUT_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white/70 px-3.5 py-2.5 text-sm text-slate-900 "
    "shadow-sm outline-none transition placeholder:text-slate-400 "
    "focus:border-blue-600 focus:bg-white focus:ring-4 focus:ring-blue-600/15"
)


class StyledFormMixin:
    """Applies the Tailwind input style to every field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = INPUT_CLASSES


class LoginForm(StyledFormMixin, AuthenticationForm):
    pass


class RegisterForm(StyledFormMixin, UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    field_order = ['first_name', 'last_name', 'username', 'birth_date', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm password'
        self.fields['birth_date'].label = 'Birth date'

    def clean_birth_date(self):
        value = self.cleaned_data['birth_date']
        if value > date.today():
            raise forms.ValidationError("Birth date can't be in the future.")
        return value

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Profile.objects.create(user=user, birth_date=self.cleaned_data['birth_date'])
        return user
