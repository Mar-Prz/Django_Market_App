from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')), #creates a url pattern for our front page, path is an empty string for front pages
    path('items/', include('item.urls')), #all urls that begin with items will automatically go into the item.urls and check if there is a path with the pk there
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('conversation.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
