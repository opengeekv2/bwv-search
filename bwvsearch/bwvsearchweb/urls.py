from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'bwvsearchweb'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
