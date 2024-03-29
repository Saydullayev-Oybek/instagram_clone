import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

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
    image = models.ImageField(upload_to='users_images/', null=True, blank=True,
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'png', 'pdf', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify(self, verify_type):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'
            while CustomUser.objects.filter(username=temp_username):
                temp_username = f'{temp_username}{random.randint(0, 9)}'
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f'password{uuid.uuid4().__str__().split("-")[-1]}'
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        print('token', refresh)
        return {
            'access': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(CustomUser, self).save(*args, **kwargs)

    def clean(self):
        self.check_username()
        self.check_email()
        self.check_pass()
        self.hashing_password()


PHONE_EXPIRATION = 2
EMAIL_EXPIRATION = 5


class UserConfirmation(BaseModel):
    VERIFY_TYPE = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    verify_type = models.CharField(max_length=31, choices=VERIFY_TYPE)
    code = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verify_code')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_PHONE:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRATION)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRATION)
        super(UserConfirmation, self).save(*args, **kwargs)
