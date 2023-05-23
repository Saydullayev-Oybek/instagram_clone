from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator

from shared.utility import send_mail, send_phone_code
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shared.utility import check_email_or_phone
from .models import CustomUser, CODE_VERIFIED, DONE, PHOTO_STEP

VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(CustomUserSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'auth_type',
            'auth_status',
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        if user.auth_type == VIA_PHONE:
            code = user.create_verify(VIA_PHONE)
            send_mail(user.phone_number, code)
            # send_phone_code(user.phone_number, code)
        elif user.auth_type == VIA_EMAIL:
            code = user.create_verify(VIA_EMAIL)
            send_mail(user.email, code)
        user.save()
        return user

    def validate(self, data):
        super(CustomUserSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        if input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif input_type == 'phone':
            data = {
                'phone_number': input_type,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': 'Tel raqam yoki email xato'
            }
            raise ValidationError(data)
        return data

    def validate_email_phone_number(self, value):
        value = str(value.lower())
        if value and CustomUser.objects.filter(phone_number=value).exists():
            data = {
                'success': False,
                'message': 'Bu raqamdan avval foydalanilgan'
            }
            raise ValidationError(data)

        elif value and CustomUser.objects.filter(email=value).exists():
            data = {
                'success': False,
                'message': 'Bu emaildan avval foydalanilgan'
            }
            raise ValidationError(data)
        return value

    # def to_representation(self, instance):
    #     print('to_rep', instance)
    #     data = super(CustomUserSerializer, self).to_representation(instance)
    #     token_value = instance.token()
    #     print('token', token_value)
    #     data.update(token_value)
    #
    #     return data
    def to_representation(self, instance):
        data = super(CustomUserSerializer, self).to_representation(instance)

        # Access the user object from the serializer context
        user = self.context['request'].user

        # Retrieve the user token
        token = user.token() if hasattr(user, 'token') else None
        # token = instance.token()

        # Add the token value to the serialized data
        data['tokens'] = token

        return data


class ChangeUserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password != confirm_password:
            raise ValidationError(
                {
                    'message': 'password is not same with confirm password'
                }
            )
        if password:
            validate_password(password)
            validate_password(confirm_password)
        return data

    def validate_username(self, username):
        if username < 5 or username > 30:
            raise ValidationError(
                {
                    'message': 'username must contain between 5 to 30'
                }
            )
        if username.isdigit():
            raise ValidationError(
                {
                    'message': 'username entirely only numeric'
                }
            )
        return username

    def validate_first_name(self, first_name):
        if first_name.isdigit():
            raise ValidationError(
                {
                    'message': 'first_name entirely only numeric'
                }
            )
        if first_name < 5 or first_name > 30:
            raise ValidationError(
                {
                    'message': 'first name must contain between 5 to 30'
                }
            )
        return first_name

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.password = validated_data.get('password')
        if validated_data.get('password'):
            instance.password.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()
        return instance

class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'pdf', 'heic', 'heif'
    ])])

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')

        if photo:
            instance.photo = photo
            instance.auth_status = PHOTO_STEP
            instance.save()
        return instance

