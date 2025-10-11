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

]
