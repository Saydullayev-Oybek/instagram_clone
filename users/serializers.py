from shared.utility import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shared.utility import check_email_or_phone
from .models import CustomUser
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
        print(user)
        if user.auth_type == VIA_PHONE:
            code = user.create_verify(VIA_PHONE)
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

