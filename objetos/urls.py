from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('registrar_devolucao/', views.registrar_devolucao, name='registrar_devolucao'),
    path('criar_conta/', views.criar_conta, name='criar_conta'),
]
