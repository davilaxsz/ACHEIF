from django.shortcuts import render, get_object_or_404, redirect 
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Objeto, Categoria, Local
from .forms import ObjetoForm, CategoriaForm, LocalForm, ObjetoFiltroForm
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    objetos_recentes = Objeto.objects.select_related('categoria').order_by('-data_achado')[:5]

    return render(request, "objetos/inicio.html", {
        'objetos_recentes': objetos_recentes,
    })


def relatorios(request):
    return render(request, "objetos/relatorios.html")

def registrar_devolucao(request):
    return render(request, "objetos/registrar_devolucao.html")

#CRUD OBJETOS 

def criar_objeto(request):
    if request.method == 'POST':
        form = ObjetoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_objetos')
    else:
        form = ObjetoForm()
    
    categorias = Categoria.objects.all()
    locais = Local.objects.all()

    return render(request, 'objetos/criar_objeto.html', {
        'form': form,
        'categorias': categorias,
        'locais': locais,
    })



def listar_objetos(request):

    objetos = Objeto.objects.all().select_related('categoria')

    filtro_form = ObjetoFiltroForm(request.GET or None)

    if filtro_form.is_valid():

        nome = filtro_form.cleaned_data.get('nome')
        if nome:
            objetos = objetos.filter(tipo__icontains=nome)

        categoria = filtro_form.cleaned_data.get('categoria')
        if categoria:
            objetos = objetos.filter(categoria=categoria)

        local = filtro_form.cleaned_data.get('local')
        if local:
            objetos = objetos.filter(local_achado=local)

    paginator = Paginator(objetos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'objetos/listar_objetos.html', {
        'objetos': page_obj,
        'page_obj': page_obj,
        'filtro_form': filtro_form,

        # 🔥 AGORA SIM você manda para o template:
        'categorias': Categoria.objects.all(),
        'locais': Local.objects.all(),

        'querystring': request.GET.urlencode(),
    })


def editar_objeto(request, id):
    objeto = get_object_or_404(Objeto, pk=id)
    categorias = Categoria.objects.all()
    locais = Local.objects.all()

    if request.method == 'POST':
        form = ObjetoForm(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Objeto editado com sucesso.")
            return redirect('objetos:listar_objetos')
        else:
            messages.error(request, "Por favor corrija os erros abaixo.")
    else:
        form = ObjetoForm(instance=objeto)

    return render(request, 'objetos/criar_objeto.html', {
        'form': form,
        'objeto': objeto,
        'categorias': categorias,
        'locais': locais,
    })

@require_POST
def apagar_objeto(request, id):
    objeto = get_object_or_404(Objeto, pk=id)
    objeto.delete()
    return redirect('objetos:listar_objetos')

#CRUD CATEGORIA

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'objetos/categoria/listar_categorias.html', {'categorias': categorias})

def criar_categoria(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect('objetos:criar_objeto')
    else:
        form = CategoriaForm()

    return render(request, 'objetos/categoria/criar_categoria.html', {
        'form': form,
        'next': next_url
    })

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'objetos/categoria/criar_categoria.html', {'form': form, 'categoria': categoria})

def apagar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('objetos:listar_categorias')
    return render(request, 'objetos/confirma_apagar_categoria.html', {'categoria': categoria})

#CRUD LOCAL 
def listar_locais(request):
    locais = Local.objects.all()
    return render(request, 'objetos/local/listar_locais.html', {'locais': locais})

def criar_local(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect('objetos:listar_locais')
    else:
        form = LocalForm()

    return render(request, 'objetos/local/criar_local.html', {
        'form': form,
        'next': next_url
    })
def editar_local(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_locais')
    else:
        form = LocalForm(instance=local)
    return render(request, 'objetos/local/criar_local.html', {'form': form, 'local': local})

@require_POST
def apagar_local(request, pk):
    local = get_object_or_404(Local, pk=pk)
    local.delete()
    return redirect('objetos:listar_locais')

