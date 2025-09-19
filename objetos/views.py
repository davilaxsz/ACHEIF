from django.shortcuts import render

def dashboard(request):
    contexto = {
        "total_itens": 10,
        "perdidos": 4,
        "encontrados": 5,
        "devolvidos": 1,
    }
    return render(request, "objetos/dashboard.html", contexto)

def relatorios(request):
    return render(request, "objetos/relatorios.html")

def registrar_devolucao(request):
    return render(request, "objetos/registrar_devolucao.html")

def criar_conta(request):
    return render(request, "objetos/criar_conta.html")

