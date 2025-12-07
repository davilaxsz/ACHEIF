from django.urls import path
from . import views

app_name = 'usuarios'  

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('listar_objetos/', views.listar_objetos, name='listar_objetos'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/deletar/<int:user_id>/', views.deletar_usuario, name='deletar_usuario'),
]

