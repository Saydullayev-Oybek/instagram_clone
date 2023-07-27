from django.urls import path
from .views import (
    PostAPIView,
    PostCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    PostLikesAPIView,
    CommentRetrieveUpdateDestroyApiView,
    CommentLikesAPIView,
    CommentLikesCreateAPIView,
    PostLikesCreateAPIView,
)

urlpatterns = [
    path('list/', PostAPIView.as_view()),
    path('create/', PostCreateAPIView.as_view()),
    path('likes/', PostLikesAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:pk>/likes/', PostLikesCreateAPIView.as_view()),
    path('<uuid:pk>/comments/', CommentAPIView.as_view()),
    path('<uuid:pk>/comments/create/', CommentCreateAPIView.as_view()),
    path('comments/', CommentListAPIView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveUpdateDestroyApiView.as_view()),
    path('comments/likes', CommentLikesAPIView.as_view()),
    path('comments/<uuid:pk>/likes', CommentLikesCreateAPIView.as_view()),
]
