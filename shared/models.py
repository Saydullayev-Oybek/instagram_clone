import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    uploaded_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
