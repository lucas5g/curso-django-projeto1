
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import Recipe
import os

def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except(ValueError, FileNotFoundError) as e:
        print(e)

@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    if kwargs.get("raw"):
        return 

    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance is None:
        return

    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
