from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.upload_file,name='upload'),
    path('download/<pk>',views.download_file,name='download'),
    path('list/',views.list_files,name='list'),
]