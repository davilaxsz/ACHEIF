from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

# Defina um CPF *único* e fixo para este usuário.
# Use um valor que você sabe que NUNCA será um CPF real.
# Se o CPF for um CharField, você pode usar uma string.
CPF_FIXO_ADMIN = '00000000000' # Exemplo de CPF dummy

@receiver(post_migrate)
def criar_usuario_fixo(sender, **kwargs):
    User = get_user_model()
    
    # Adicionamos uma verificação para garantir que o signal só rode
    # para o app 'usuarios', evitando execuções desnecessárias.
    if sender.name == 'usuarios':
        
        # 1. Tenta obter o usuário pelo username. Se não existir, ele o cria.
        # O 'defaults' é usado apenas na criação do objeto.
        usuario, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@exemplo.com',
                # PRECISAMOS do CPF aqui, pois é um campo UNIQUE e obrigatório
                'cpf': CPF_FIXO_ADMIN, 
                'is_superuser': True,
                'is_staff': True,
            }
        )
        
        # 2. Se o usuário já existia (created=False), garantimos que a senha e outros
        # campos que poderiam ter sido alterados sejam definidos/atualizados.
        if not created:
            usuario.is_superuser = True
            usuario.is_staff = True
            # Adicione outras atualizações de campo aqui, se necessário.

        # 3. A senha deve ser definida APENAS se tiver sido criada
        # OU se você quiser resetar a senha a cada migrate.
        # Definir a senha sempre é mais seguro para garantir que ela exista.
        usuario.set_password('admin123') 
        
        # 4. Salva o objeto (agora, se ele já existia, será um UPDATE, e não um INSERT).
        # Se foi criado, este save está implícito no get_or_create (se não for raw).
        # É seguro chamar save() aqui para garantir que a senha e atualizações sejam salvas.
        usuario.save()

        if created:
             print(f"Usuário fixo 'admin' criado com sucesso.")
        else:
             print(f"Usuário fixo 'admin' atualizado com sucesso.")





