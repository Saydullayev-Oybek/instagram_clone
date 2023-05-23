from django.urls import path
from .views import CreateUserView, VerifyAPIView, ChangeUserInfoView, ChangeUserPhotoView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    # path('new-verify/', GetNewVerifyCode.as_view()),
    path('update-user/', ChangeUserInfoView.as_view()),
    path('upload-photo/', ChangeUserPhotoView.as_view())
]