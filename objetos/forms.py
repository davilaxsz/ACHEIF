
from django import forms
from .models import Objeto, Categoria

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['tipo', 'descricao', 'data_achado', 'local_achado', 'categoria', 'status']
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
