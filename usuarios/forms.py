from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioAdaptado

class UsuarioAdaptadoCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioAdaptado
        fields = ['username', 'email', 'cpf', 'foto_perfil', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF (apenas números)'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome de usuário'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Senha'}))
class PerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioAdaptado
        fields = ['username', 'email', 'foto_perfil']  # <-- adicionamos username
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'foto_perfil': 'Foto de Perfil',
        }
