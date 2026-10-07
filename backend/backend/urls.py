from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.views import AnimalListView, AnimalCollarRetrieveView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("animales/", AnimalListView.as_view()),
    path ("collares/<str:public_id>/", AnimalCollarRetrieveView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)