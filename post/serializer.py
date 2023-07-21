from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from post.models import Post, PostLike
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'image', 'username')

class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'created_time', 'post_likes_count', 'post_comments_count', 'me_liked')

    def get_post_likes_count(self, obj):
        return obj.likes.count()

    def get_post_comments_count(self, obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        user = self.request.user
        request = self.context.get('request', None)
        if request and user.is_authenticated:
            try:
                like = PostLike.objects.get(post=obj, author=user)
                return True
            except PostLike.DoesNotExist:
                return False
        return False


