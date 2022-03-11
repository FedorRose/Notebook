from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main.views import *

router = routers.DefaultRouter()
router.register(r'note', NoteViewSet)
router.register(r'notelist', NoteListViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/note/put/<int:data>/', NoteViewSet.as_view({'post': 'partial_update'})),
    path('api/v1/notelist/put/<int:pk>/', NoteListViewSet.as_view({'post': 'partial_update'})),
    path('api/v1/notelist/delete/<int:pk>/', NoteListViewSet.as_view({'get': 'destroy'})),
    path('api/v1/', include(router.urls)),
]
