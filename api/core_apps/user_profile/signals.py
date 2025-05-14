from typing import Any, Type
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from logging import getLogger
from config.settings.base import AUTH_USER_MODEL
from core_apps.user_profile.models import Profile

logger = getLogger(__name__)

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs: Any) -> None:
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.username}")
        
@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender: Type[Model], instance: Model, **kwargs: Any) -> None:
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        logger.error(f"Profile not found for user {instance.username}")