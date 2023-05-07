from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel
# Create your models here.

ORDINARY_USER, ADMIN, MANAGER = ('ordinary_user', 'admin', 'manager')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CODE_VERIFIED, DONE, PHOTO_STEP = ('new', 'code_verified', 'done', 'photo_step')

class CustomUser(AbstractUser, BaseModel):
    USER_TYPE = [
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    ]
    AUTH_TYPE = [
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    ]
    AUTH_STATUS = [
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_STEP, PHOTO_STEP)
    ]

    user_type = models.CharField(max_length=31, choices=USER_TYPE, default=ORDINARY_USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='users_images/', null=True, blank=True)

    def __str__(self):
        return self.username