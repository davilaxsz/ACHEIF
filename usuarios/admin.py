from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAdaptado

@admin.register(UsuarioAdaptado)
class UsuarioAdaptadoAdmin(UserAdmin):
    model = UsuarioAdaptado
    list_display = ['username', 'email', 'cpf', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'groups']
    search_fields = ['username', 'email', 'cpf']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('cpf', 'foto_perfil')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('cpf', 'foto_perfil')
        }),
    )
