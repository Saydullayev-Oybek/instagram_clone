from rest_framework.generics import CreateAPIView

from post.serializer import PostSerializer


class CreatePostView(CreateAPIView):
    serializer_class = PostSerializer