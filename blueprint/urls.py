
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'BluePrint Admin'
admin.site.site_title = 'BluePrint Admin'

urlpatterns = [

    path('users/', include('user.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)