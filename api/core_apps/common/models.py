import uuid
from typing import Any, Optional
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        abstract = True
    
class ContentView(TimeStampModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
    object_id = models.UUIDField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='content_views', verbose_name=_('User'))
    viewer_ip = models.GenericIPAddressField(verbose_name=_('Viewer IP Address'), null=True, blank=True)
    last_viewed = models.DateTimeField(verbose_name=_('Last Viewed'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Content View')
        verbose_name_plural = _('Content Views')
        unique_together = ('content_type', 'object_id', 'user', 'viewer_ip')
        
    def __str__(self) -> str:
        return f"{self.user.get_full_name()} viewed {self.content_object} from {self.viewer_ip}"
    
    @classmethod
    def record_view(cls, content_object: Any, user: Optional[User] = None, viewer_ip: Optional[str] = None) -> None:
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.id,
                defaults={
                    'user': user,
                    'viewer_ip': viewer_ip,
                    'last_viewed': timezone.now()
                }
            )
            if not created:
                view.last_viewed = timezone.now()
                view.save()
        except IntegrityError:
            pass
        
        