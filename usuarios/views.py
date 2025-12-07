from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UsuarioAdaptadoCreationForm, LoginForm, PerfilForm
from django.contrib.auth.models import Group
from objetos.models import Objeto, Categoria
from django.core.paginator import Paginator

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('usuarios:login')
    else:
        form = UsuarioAdaptadoCreationForm()
    
    return render(request, 'usuarios/cadastrar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.username == "admin_fixo":
            return redirect('objetos:dashboard')  # vai para dashboard do admin fixo
        elif request.user.groups.filter(name='USUARIO_SIMPLES').exists():
            return redirect('usuarios:listar_objetos')  # vai para tela de usuários normais
        else:
            return redirect('objetos:dashboard')  # outros admins

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')

                if user.username == "admin_fixo":
                    return redirect('objetos:dashboard')
                elif user.groups.filter(name='USUARIO_SIMPLES').exists():
                    return redirect('usuarios:listar_objetos')
                else:
                    return redirect('objetos:dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('usuarios:login') 

@login_required
def perfil_view(request):
    user = request.user #usuario logado
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilForm(instance=user)
    
    return render(request, 'usuarios/perfil.html', {'form': form, 'user': user})

#Tela exclusiva para usuários
@login_required
def listar_objetos(request):
    q = request.GET.get('q', '')  # pega o valor da barra de pesquisa
    categoria_id = request.GET.get('categoria', '')
    local_achado = request.GET.get('local', '')
    objetos = Objeto.objects.all().order_by('-data_achado')

    if q:
        objetos = objetos.filter(tipo__icontains=q)
    if categoria_id:
        objetos = objetos.filter(categoria__id=categoria_id)
    if local_achado:
        objetos = objetos.filter(local_achado=local_achado)

    paginator = Paginator(objetos, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'objetos': page_obj, 
        'q': q,
        'categoria_id': categoria_id,
        'local_achado': local_achado,
        'categorias': Categoria.objects.all(),
        'locais': Objeto.objects.values_list('local_achado', flat=True).distinct()
    }

    return render(request, 'usuarios/listar_objetos.html', context) 

def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def listar_usuarios(request):
    #caso coloque filtro
    User = get_user_model()
    q = request.GET.get('q', '')

    usuarios = User.objects.all().order_by('username')

    if q:
        usuarios = usuarios.filter(username__icontains=q)

    paginator = Paginator(usuarios, 10)  # 10 usuários por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'usuarios': page_obj,
        'q': q
    }
    return render(request, 'usuarios/listar_usuarios.html', context)


@login_required
@superuser_required
def deletar_usuario(request, user_id):
    User = get_user_model()
    usuario = get_object_or_404(User, id=user_id)
    if usuario.is_superuser:
        messages.error(request, "Não é possível deletar o superusuário.")
        return redirect('usuarios:listar_usuarios')
    usuario.delete()
    messages.success(request, f"Usuário {usuario.username} deletado com sucesso!")
    return redirect('usuarios:listar_usuarios')