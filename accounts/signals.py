from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from accounts.models import Profile


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.label != "accounts":
        return

    regular_users, _ = Group.objects.get_or_create(name="Regular Users")
    recipe_editors, _ = Group.objects.get_or_create(name="Recipe Editors")

    regular_permissions = Permission.objects.filter(
        content_type__app_label="recipes",
        codename__in=[
            "view_recipe",
            "add_recipe",
        ],
    )
    regular_users.permissions.add(*regular_permissions)

    recipe_permissions = Permission.objects.filter(
        content_type__app_label="recipes",
        codename__in=[
            "add_recipe",
            "change_recipe",
            "delete_recipe",
            "view_recipe",
        ],
    )
    recipe_editors.permissions.add(*recipe_permissions)


@receiver(post_save, sender=get_user_model())
def assign_regular_user_group(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        regular_users, _ = Group.objects.get_or_create(name="Regular Users")
        instance.groups.add(regular_users)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        Profile.objects.get_or_create(user=instance)
