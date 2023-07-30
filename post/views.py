from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializer import PostSerializer, PostCommentSerializer, PostLikeSerializer, CommentLikeSerializer
from shared.custom_pagination import CustomPagination
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


class CommentListAPIView(generics.ListAPIView):
    serializer_class = PostCommentSerializer(many=True)
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return PostComment.objects.all()


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


class PostLikesCreateAPIView(APIView):

    def post(self, pk):
        try:
            post_like = PostLike.objects.get(
                author=self.request.user,
                post_id=pk
            )
            post_like.delete()
            data = {
                'success': True,
                'message': 'Like successfully deleted',
                'data': None
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExists:
            post_like = PostLike.objects.create(
                author=self.request.user,
                post_id=pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                'success': True,
                'message': 'Put like this post',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)


class CommentLikesCreateAPIView(APIView):

    def post(self, pk):
        try:
            comment_like = CommentLike.objects.get(
                author=self.request.user,
                comment_id=pk
            )
            comment_like.delete()
            data = {
                'success': True,
                'message': 'Like successfully deleted',
                'data': None
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExists:
            comment_like = CommentLike.objects.create(
                author=self.request.user,
                comment_id=pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                'success': True,
                'message': 'Put like this comment',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
