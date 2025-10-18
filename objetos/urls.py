from django.urls import path
from . import views

app_name = 'objetos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # dashboard separado
    path('relatorios/', views.relatorios, name='relatorios'),
    path('registrar_devolucao/', views.registrar_devolucao, name='registrar_devolucao'),
    path('criar_objeto/', views.criar_objeto, name='criar_objeto'),
    path('listar_objetos/', views.listar_objetos, name='listar_objetos'),
    path('editar/<int:id>/', views.editar_objeto, name='editar_objeto'),
    path('apagar/<int:id>/', views.apagar_objeto, name='apagar_objeto'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/apagar/', views.apagar_categoria, name='apagar_categoria'),
    path('local/', views.listar_locais, name='listar_locais'),
    path('local/criar/', views.criar_local, name='criar_local'),
    path('local/<int:pk>/editar/', views.editar_local, name='editar_local'),
    path('local/<int:pk>/apagar/', views.apagar_local, name='apagar_local'),

]
