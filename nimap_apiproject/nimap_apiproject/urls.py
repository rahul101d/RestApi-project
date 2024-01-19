"""
URL configuration for nimap_apiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from api import views
from rest_framework.authtoken import views as v1
from rest_framework.routers import DefaultRouter

router=DefaultRouter() 
router.register('client_api', views.client_viewset, basename='client')
router.register('project_api', views.project_viewset, basename='project')
router.register('client_details', views.clientdetails_viewset, basename='client_details')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("register/", views.register, name="register"),
    path('api/',include(router.urls)),
    path('api/project_api/<int:id>',views.project_viewset.as_view({"post":"create"})),
    path('api/',include(router.urls)),
    path('api/client_details/<int:id>',views.clientdetails_viewset.as_view({"get":"list"})),    
]
