
from django import forms
from .models import Objeto, Categoria, Local, Devolucao

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['tipo', 'descricao', 'foto', 'categoria', 'local_achado', 'data_achado', 'status']
        widgets = {
            'data_achado': forms.DateInput(attrs={'type': 'date'}),
        }



class ObjetoFiltroForm(forms.Form):
    nome = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome...'
        }),
        label='Nome'
    )

    categoria = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Categoria (ex: Eletrônico, Documento...)'
        }),
        label='Categoria'
    )

    local = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Local onde foi encontrado...'
        }),
        label='Local'
    )


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

class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = ['nome_retirante', 'cpf_retirante', 'data_devolucao'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do '}),
        }
        labels = {
            'nome': 'Nome do Local',
        }

