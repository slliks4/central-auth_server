import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=17)
    
    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return super().__str__()