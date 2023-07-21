from datetime import datetime

from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shared.utility import send_mail
from .models import CustomUser, NEW, CODE_VERIFIED, VIA_EMAIL, VIA_PHONE
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .serializers import CustomUserSerializer, ChangeUserInfoSerializer, ChangeUserPhotoSerializer


class CreateUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomUserSerializer


class VerifyAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_code(user, code)
        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_code(user, code):
        verifies = user.verify_code(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'message': 'parol xato yoki eskirgan'
            }
            raise ValidationError(data)
        else:
            verifies['is_confirmed'] = True
            print(verifies)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerifyCode(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify(VIA_EMAIL)
            send_mail(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify(VIA_PHONE)
            send_mail(user.phone_number, code)
        else:
            data = {
                'success': False,
                'message': 'email yoki telefon raqam xato'
            }
            return ValidationError(data)
        return Response(
            {
                'success': True,
                'message': 'Tasdiqlash kodingiz boshqatdan konatildi'
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_code(expiration_time__gte=datetime.now(), is_confirmed=False)
        print(verifies)
        if verifies.exists():
            data = {
                'message': 'Kodingiz holi ishlatish uchun yaroqli, biroz kutb turing'
            }
            return ValidationError(data)

class ChangeUserInfoView(UpdateAPIView):
    permission_classes = [AllowAny, ]
    serializer_classes = ChangeUserInfoSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInfoView, self).update(self, *args, **kwargs)
        data = {
            'success': True,
            'message': 'User updated successfully',
            'auth_status': self.request.user.auth_status,
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInfoView, self).partial_update(request, *args, **kwargs)

        data = {
            'success': True,
            'message': 'User updated successfully',
            'auth_status': self.request.user.auth_status
        }
        return Response(data, status=200)

class ChangeUserPhotoView(APIView):

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            serializer.save()
            return Response(
                {
                'message': 'picture uploaded successfully'
                }, status=200)
        return Response(
            serializer.errors, status=400
            )
