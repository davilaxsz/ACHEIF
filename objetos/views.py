from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Objeto
from .forms import ObjetoForm

def dashboard(request):
    return render(request, "objetos/inicio.html")

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
    return render(request, 'objetos/criar_objeto.html', {'form': form})

def listar_objetos(request):
    objetos = Objeto.objects.all().select_related('categoria')
    return render(request, 'objetos/listar_objetos.html', {'objetos': objetos})

def editar_objeto(request, id):
    objeto = get_object_or_404(Objeto, pk=id)
    if request.method == 'POST':
        form = ObjetoForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_objetos')
    else:
        form = ObjetoForm(instance=objeto)
    return render(request, 'objetos/criar_objeto.html', {'form': form, 'objeto': objeto})

@require_POST
def apagar_objeto(request, id):
    objeto = get_object_or_404(Objeto, pk=id)
    objeto.delete()
    return redirect('objetos:listar_objetos')

#CRUD CATEGORIA

from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'objetos/listar_categorias.html', {'categorias': categorias})

def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'objetos/form_categoria.html', {'form': form})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'objetos/form_categoria.html', {'form': form, 'categoria': categoria})

def apagar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('objetos:listar_categorias')
    return render(request, 'objetos/confirma_apagar_categoria.html', {'categoria': categoria})

