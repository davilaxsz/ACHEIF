from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdaptadoCreationForm, LoginForm,PerfilForm
from django.contrib.auth.models import Group


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Adicionar usuário ao grupo USUARIO_SIMPLES por padrão
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UsuarioAdaptadoCreationForm()
    
    return render(request, 'usuarios/cadastrar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('objetos:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                
                # Redireciona para a página solicitada ou para listar_vagas
                next_page = request.GET.get('next', 'objetos:dashboard')
                return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')

@login_required
def perfil_view(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'usuarios/perfil.html', {'form': form})