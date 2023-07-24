from django.urls import path
from .views import PostAPIView, PostCreateAPIView, PostRetrieveUpdateDestroyAPIView, CommentAPIView, CommentCreateAPIView

urlpatterns = [
    path('posts/', PostAPIView.as_view()),
    path('posts/create/', PostCreateAPIView.as_view()),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<uuid:pk>/comments/', CommentAPIView.as_view()),
    path('posts/<uuid:pk>/comments/create/', CommentCreateAPIView.as_view()),
]