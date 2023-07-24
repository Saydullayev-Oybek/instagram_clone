from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from shared.custom_pagination import CustomPagination
from post.serializer import PostSerializer, PostCommentSerializer, PostLikeSerializer, CommentLikeSerializer
from .models import Post, PostComment, PostLike, CommentLike


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


class CommentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PostComment.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.serializer_class(comment, self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': 'Comment successfully updated',
                'data': serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Comment successfully deleted'
            }
        )


class PostLikesAPIView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PostLike.objects.all()
        return queryset


class PostRetrieveLikesAPIView(generics.ListCreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostLike.objects.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentLikesAPIView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = CommentLike.objects.all()
        return queryset


class CommentRetrieveLikesAPIView(generics.ListCreateAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        queryset = CommentLike.objects.filter(comment__id=comment_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
