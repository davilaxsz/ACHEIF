from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Objeto(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando Devolução'),
        ('devolvido', 'Devolvido'),
    ]

    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_achado = models.DateField()
    local_achado = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="objetos"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando')

    def __str__(self):
        return f"{self.tipo} ({self.get_status_display()})"


class Devolucao(models.Model):
    objeto = models.OneToOneField(
        Objeto, on_delete=models.CASCADE, related_name="devolucao"
    )
    nome_retirante = models.CharField(max_length=100)
    cpf_retirante = models.CharField(max_length=14)  
    data_devolucao = models.DateField()

    def __str__(self):
        return f"Devolução de {self.objeto.tipo} para {self.nome_retirante}"
    
class Local(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome

 

