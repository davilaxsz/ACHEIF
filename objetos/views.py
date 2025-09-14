from django.shortcuts import render

def dashboard(request):
    contexto = {
        "total_itens": 10,
        "perdidos": 4,
        "encontrados": 5,
        "devolvidos": 1,
    }
    return render(request, "objetos/dashboard.html", contexto)

