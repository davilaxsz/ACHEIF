from django.contrib import admin
from .models import Categoria, Objeto, Devolucao, Local

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "criado_em", "atualizado_em")
    search_fields = ("nome",)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "categoria", "status", "data_achado", "local_achado")
    list_filter = ("status", "categoria")
    search_fields = ("tipo", "descricao", "local_achado")
    autocomplete_fields = ("categoria",)  # campo categoria vira busca inteligente


@admin.register(Devolucao)
class DevolucaoAdmin(admin.ModelAdmin):
    list_display = ("objeto", "nome_resgate", "cpf_resgate", "data_devolucao")
    search_fields = ("nome_resgate", "cpf_resgate")

