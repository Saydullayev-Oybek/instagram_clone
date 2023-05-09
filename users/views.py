from .models import CustomUser
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from .serializers import CustomUserSerializer

class CreateUserView(CreateAPIView):
    queryset = CustomUser.objects.all
    permission_classes = (permissions.AllowAny, )
    serializer_class = CustomUserSerializer