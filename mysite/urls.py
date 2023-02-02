from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from user.views import myInfo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pet.urls')),
    path('me/',myInfo),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('',include('djoser.urls.authtoken')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
