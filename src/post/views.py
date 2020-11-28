from django.db.models import Q

from post.models import Post
from post.serializers import PostSerializer
from utils import views


class PostViewSet(views.DreamerViewSet):
    serializer_class = PostSerializer
    filter_fields = ['user__username', 'status']

    def get_queryset(self):
        if self.action in ['destroy', 'update']:
            return Post.objects.filter(user_id=self.request.user.id)
        return Post.objects.filter(Q(user_id=self.request.user.id) | Q(status=Post.STATUS.published))
