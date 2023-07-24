from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rich.status import Status

from shared.custom_pagination import CustomPagination
from post.serializer import PostSerializer, PostCommentSerializer, PostLikeSerializer, CommentLikeSerializer
from .models import Post, PostLike, PostComment, CommentLike


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': 'Post successfully updated',
                'data': serializer.data,
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Post successfully deleted'
            }
        )


class CommentAPIView(generics.ListAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        serializer.save(author=self.request.user, post_id=post_id)
        return queryset