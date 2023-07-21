from rest_framework import serializers

from post.models import Post, PostLike, PostComment
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
        fields = [
            'id',
            'author',
            'image',
            'caption',
            'created_time',
            'post_likes_count',
            'post_comments_count',
            'me_liked'
        ]

    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                PostLike.objects.get(post=obj, author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False
        return False


class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    me_liked = serializers.SerializerMethodField('get_me_liked')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = PostComment
        fields = [
            'id',
            'author',
            'comment',
            'parent',
            'replies',
            'me_liked',
            'likes_count'
        ]

    def get_replies(self, obj):
        if obj.child.exists():
            serializers = self.__class__(obj.child.all, many=True, context=self.context)
            return serializers
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return None

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post')


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'comment')

