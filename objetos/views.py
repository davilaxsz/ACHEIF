from django.shortcuts import render, get_object_or_404, redirect 
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Objeto, Categoria, Local, Devolucao
from .forms import ObjetoForm, CategoriaForm, LocalForm, ObjetoFiltroForm, DevolucaoForm
from django.core.paginator import Paginator
from django.db.models import Q


def dashboard(request):
    #BUSCA
    q = request.GET.get("q")  # termo digitado

    objetos_recentes = Objeto.objects.order_by('-data_achado')

    if q:
        objetos_recentes = objetos_recentes.filter(tipo__icontains=q)  # somente pelo nome

    objetos_recentes = objetos_recentes[:5]  # mantém só os 5 mais recentes filtrados

    #CONTADORES DASHBOARD
    total_objetos_perdidos = Objeto.objects.filter(status='aguardando').count()
    total_objetos_achados = Objeto.objects.filter(status='achado').count()
    total_devolucoes = Devolucao.objects.count()

    context = {
        'total_objetos_perdidos': total_objetos_perdidos,
        'total_objetos_achados': total_objetos_achados,
        'total_devolucoes': total_devolucoes,
        'objetos_recentes': objetos_recentes,
        'q': q,  
    }
    return render(request, 'objetos/inicio.html', context)


#CRUD OBJETOS 

def criar_objeto(request):
    if request.method == 'POST':
        form = ObjetoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('objetos:listar_objetos')
    else:
        form = ObjetoForm()
    
    categorias = Categoria.objects.all() #para filtros posteriormente
    locais = Local.objects.all()

    return render(request, 'objetos/criar_objeto.html', {
        'form': form,
        'categorias': categorias,
        'locais': locais,
    })


def listar_objetos(request):
    objetos = Objeto.objects.all().order_by('-data_achado') 
    categorias = Categoria.objects.all()
    locais = Local.objects.all()

    # Filtros por categoria e local
    categoria_selecionada = request.GET.get('categoria', '')
    local_selecionado = request.GET.get('local', '')

    if categoria_selecionada:
        objetos = objetos.filter(categoria__id=categoria_selecionada)
    if local_selecionado:
        objetos = objetos.filter(local_achado=local_selecionado)

    # Paginação
    paginator = Paginator(objetos, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'objetos/listar_objetos.html', {
        'objetos': page_obj.object_list,
        'page_obj': page_obj,
        'categorias': categorias,
        'locais': locais,
        'categoria_id': categoria_selecionada,
        'local_achado': local_selecionado,
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

from django.core.paginator import Paginator

def listar_categorias(request):
    categorias = Categoria.objects.all()

    paginator = Paginator(categorias, 10)  # número de itens por página
    page_number = request.GET.get("page")  # captura ?page=2 etc.
    page_obj = paginator.get_page(page_number)

    contexto = {
        "page_obj": page_obj,
        "categorias": page_obj.object_list,  # opcional, caso o template use
    }

    return render(request, "objetos/categoria/listar_categorias.html", contexto)


def criar_categoria(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect('objetos:listar_categorias')
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
    locais = Local.objects.all().order_by('nome')  # opcional: ordena por nome

    paginator = Paginator(locais, 10)  # 10 locais por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'objetos/local/listar_locais.html', {
        'locais': page_obj.object_list,
        'page_obj': page_obj,
    })

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
#CRUD DEVOLUCAO

def listar_devolucao(request):
    devolucoes = Devolucao.objects.select_related('objeto').all().order_by('-data_devolucao')

    # Filtros
    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')

    if busca:
        devolucoes = devolucoes.filter(nome_resgate__icontains=busca)
    if status:
        if status == 'pendente':
            devolucoes = devolucoes.filter(objeto__status='aguardando')
        elif status == 'devolvido':
            devolucoes = devolucoes.filter(objeto__status='devolvido')

    # Paginação
    paginator = Paginator(devolucoes, 10)  # 9 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'objetos/devolucao/listar_devolucao.html', {
        'devolucoes': page_obj,  # aqui devolucoes = page_obj
        'page_obj': page_obj,
        'busca': busca,
        'status': status,
    })


def criar_devolucao(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            devolucao = form.save(commit=False)
            objeto = devolucao.objeto

            # segurança extra: verificar se o objeto já foi devolvido
            if objeto.status == 'devolvido':
                messages.error(request, "Este objeto já foi devolvido!")
                return redirect("objetos:listar_devolucao")

            # atualizar status do objeto
            objeto.status = "devolvido"
            objeto.save()

            devolucao.save()
            messages.success(request, "Devolução registrada com sucesso!")

            return redirect(next_url or "objetos:listar_devolucao")
    else:
        form = DevolucaoForm()

    return render(request, "objetos/devolucao/criar_devolucao.html", {
        "form": form,
        "next": next_url,
    })


def editar_devolucao(request, pk):
    devolucao = get_object_or_404(Devolucao, pk=pk)
    objeto_antigo = devolucao.objeto

    if request.method == 'POST':
        form = DevolucaoForm(request.POST, instance=devolucao)
        if form.is_valid():
            devolucao_atualizada = form.save(commit=False)
            objeto_novo = devolucao_atualizada.objeto

            # Se mudou de objeto, atualizar status dos objetos
            if objeto_antigo != objeto_novo:
                objeto_antigo.status = "aguardando"
                objeto_antigo.save()

                objeto_novo.status = "devolvido"
                objeto_novo.save()

            devolucao_atualizada.save()
            messages.success(request, "Devolução editada com sucesso!")
            return redirect('objetos:listar_devolucao')
    else:
        form = DevolucaoForm(instance=devolucao)

    return render(request, 'objetos/devolucao/criar_devolucao.html', {
        'form': form,
        'devolucao': devolucao
    })

@require_POST
def apagar_devolucao(request, pk):
    devolucao = get_object_or_404(Devolucao, pk=pk)

    # Reverter status do objeto
    objeto = devolucao.objeto
    objeto.status = "aguardando"
    objeto.save()

    devolucao.delete()
    messages.success(request, "Devolução apagada com sucesso!")
    return redirect('objetos:listar_devolucao')

