from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

CPF_FIXO_ADMIN = '00000000000' 

@receiver(post_migrate)
def criar_usuario_fixo(sender, **kwargs):
    User = get_user_model()
    
    if sender.name == 'usuarios':
        usuario, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@exemplo.com',
                'cpf': CPF_FIXO_ADMIN, 
                'is_superuser': True,
                'is_staff': True,
            }
        )
        
        if not created:
            usuario.is_superuser = True
            usuario.is_staff = True
          
        usuario.set_password('admin123') 
        
        usuario.save()

        if created:
             print(f"Usuário fixo 'admin' criado com sucesso.")
        else:
             print(f"Usuário fixo 'admin' atualizado com sucesso.")





