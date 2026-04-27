from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        error_messages={
            'required': 'İstifadəçi adı mütləqdir.',
            'max_length': 'İstifadəçi adı çox uzundur.',
        }
    )
    full_name = forms.CharField(
        max_length=150,
        error_messages={'required': 'Ad Soyad mütləqdir.'}
    )
    phone = forms.CharField(max_length=20, required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': 'Şifrə mütləqdir.'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': 'Şifrənin təkrarı mütləqdir.'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu istifadəçi adı artıq mövcuddur.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')
        if p1 and len(p1) < 6:
            raise forms.ValidationError('Şifrə ən azı 6 simvol olmalıdır.')
        return cleaned
