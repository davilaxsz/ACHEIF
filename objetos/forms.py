
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
        fields = ['objeto', 'nome_resgate', 'cpf_resgate', 'data_devolucao']
        widgets = {
            'objeto': forms.Select(attrs={'class': 'form-control'}),
            'nome_resgate': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_resgate': forms.TextInput(attrs={'class': 'form-control'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['objeto'].queryset = Objeto.objects.filter(
            devolucao__isnull=True,      # não tem devolução
            status='aguardando'          # ou o status que você usa
        )


