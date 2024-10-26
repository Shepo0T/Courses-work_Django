from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('mailings.urls', 'mailings'), namespace='mailings')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
