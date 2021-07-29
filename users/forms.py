from django import forms
from .models import User, Contact


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserDetailForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=25, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class UserContactsForm(forms.ModelForm):
    phone = forms.RegexField(label='Phone', required=True, regex=r'^\+?1?\d{9,15}$',
                             error_messages={
                                 'invalid': 'Phone number must be entered in the format: "+999999999". Up to 15 digits '
                                 'allowed.'})
    telegram = forms.RegexField(label='Telegram', regex=r'.*?\B@[a-zA-Z0-9_]{5}.*',
                                error_messages={
                                 'invalid': 'Telegram username must be entered in the format: "@username.'},
                                required=False)
    city = forms.CharField(label='City', max_length=50)
    street = forms.CharField(label='Street', max_length=100, required=False)
    house = forms.CharField(label='House', max_length=15, required=True)
    structure = forms.CharField(label='Structure', max_length=15, required=False)
    building = forms.CharField(label='Building', max_length=15, required=False)
    apartment = forms.CharField(label='Apartment', max_length=15, required=False)

    class Meta:
        model = Contact
        fields = ('phone', 'telegram', 'city', 'street', 'house', 'structure', 'building', 'apartment',)
