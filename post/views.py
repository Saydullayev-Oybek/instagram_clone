from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from shared.custom_pagination import CustomPagination
from post.serializer import PostSerializer, PostCommentSerializer, PostLikeSerializer, CommentLikeSerializer
from .models import Post, PostLike, PostComment, CommentLike


class PostApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()

