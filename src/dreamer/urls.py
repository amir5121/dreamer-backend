from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^api/(?P<version>(v1|v2))/auth/', include('djoser.urls')),
    re_path('^api/(?P<version>(v1|v2))/auth/', include('djoser.urls.jwt')),
    re_path('^api/(?P<version>(v1|v2))/utils/', include('utils.urls')),
    re_path('^api/(?P<version>(v1|v2))/user/', include('user.urls')),
    re_path('^api/(?P<version>(v1|v2))/post/', include('post.urls')),
]
