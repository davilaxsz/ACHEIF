
from django import forms
from .models import Objeto, Categoria, Local

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['tipo', 'descricao', 'foto', 'categoria', 'local_achado', 'data_achado', 'status']
        widgets = {
            'data_achado': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']  # só esses dois para o formulário
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome']  # campos que vão aparecer no form
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do local'}),
        }
        labels = {
            'nome': 'Nome do Local',
        }

