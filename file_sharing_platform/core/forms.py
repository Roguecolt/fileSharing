from django import forms
from django.contrib.auth.models import User
from .models import File,SharedFile 

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Comfirm password'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# core/forms.py (partial update)
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'uploaded_file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'File name'}),
            'uploaded_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ShareFileForm(forms.ModelForm):
    shared_with = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Share with",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = SharedFile
        fields = ['shared_with']
    