"""DAlphaFS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from .views import shared_dir
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.shared_dir,name='shared_dir'),
    path('dir_traversal<path:dir>',views.dir_traversal,name='dir_traversal'),
    path('deleteFile<path:file_name>',views.deleteFile,name="deleteFile"),
    path('uploadFiletoDir',views.uploadFiletoDir,name="uploadFiletoDir"),
    path('download<path:file_to_download>',views.download,name="download"),
    path('deleteFolder<path:folder_name>',views.deleteFolder,name="deleteFolder"),
    path('make_dir',views.make_dir,name="make_dir")
]
