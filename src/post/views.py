from django.db.models import Q

from post.models import Post
from post.serializers import PostSerializer
from utils import views


class PostViewSet(views.DreamerViewSet):
    serializer_class = PostSerializer
    filter_fields = ["user__username", "status"]

    def get_queryset(self):
        posts_filters = dict()
        if "show_multi" in self.request.GET:
            if self.request.GET['show_multi'].lower() == 'true':
                posts_filters.update({'text__len__gt': 1})
            else:
                posts_filters.update({'text__len': 1})
        posts = Post.objects.filter(**posts_filters)
        if self.action in ['destroy', 'update']:
            return posts.filter(user_id=self.request.user.id)
        return posts.filter(Q(user_id=self.request.user.id) | Q(status=Post.STATUS.published))
