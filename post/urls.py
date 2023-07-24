from django.urls import path
from .views import (
    PostAPIView,
    PostCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentAPIView,
    CommentCreateAPIView,
    CommentListCreateAPIView,
)

urlpatterns = [
    path('list/', PostAPIView.as_view()),
    path('create/', PostCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:pk>/comments/', CommentAPIView.as_view()),
    path('<uuid:pk>/comments/create/', CommentCreateAPIView.as_view()),
    path('comments/', CommentListCreateAPIView.as_view())
]
