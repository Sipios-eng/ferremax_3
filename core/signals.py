# myapp/signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Pedido, Entrega, Producto, Contact 

@receiver(post_migrate)
def create_default_users_and_groups(sender, **kwargs):
    groups_permissions = {
        "bodeguero": [("view", Pedido)],
        "contador": [("add", Entrega)],
        "vendedor": [("view", Producto), ("change", Pedido), ("add", Contact)],
    }

    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm_action, model in permissions:
            content_type = ContentType.objects.get_for_model(model)
            codename = f"{perm_action}_{model._meta.model_name}"
            permission = Permission.objects.filter(codename=codename, content_type=content_type).first()
            group.permissions.add(permission)
            if permission:
                group.permissions.add(permission)
            else:
                print(f"Permission '{codename}' for model '{model._meta.model_name}' does not exist.")

    # Crear superusuario admin
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@gmail.com", "contrasena1")
        print("Superuser 'admin' created")

    if not User.objects.filter(username="bodeguero").exists():
        bodeguero_user = User.objects.create_user("bodeguero", "bodeguero@gmail.com", "contrasena1")
        bodeguero_user.groups.add(Group.objects.get(name="bodeguero"))
        print("User 'bodeguero' created and added to group 'bodeguero'")

 
    if not User.objects.filter(username="vendedor").exists():
        vendedor_user = User.objects.create_user("vendedor", "vendedor@gmail.com", "contrasena1")
        vendedor_user.groups.add(Group.objects.get(name="vendedor"))
        print("User 'vendedor' created and added to group 'vendedor'")


    if not User.objects.filter(username="cliente").exists():
        User.objects.create_user("cliente", "cliente@gmail.com", "contrasena1")
        print("User 'cliente' created")


    if not User.objects.filter(username="contador").exists():
        contador_user = User.objects.create_user("contador", "contador@gmail.com", "contrasena1")
        contador_user.groups.add(Group.objects.get(name="contador"))
        print("User 'contador' created and added to group 'contador'")
