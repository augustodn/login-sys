from django import forms
from users.models import User

# Create your forms here.

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput,
        }

    #Add an extra field to the login form, imported from models
    verify = forms.CharField(max_length=75, widget=forms.PasswordInput)

    def clean_verify(self):
        verify = self.cleaned_data['verify']
        password = self.cleaned_data['password']
        if verify != password:
            raise forms.ValidationError("Password don't match")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("User already exists")
        except User.DoesNotExist:
            pass

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("e-mail already exists")
        except User.DoesNotExist:
            pass

        return email
