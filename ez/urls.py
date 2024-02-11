from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("", include("backend.urls")),
    path('api-token-auth/', views.obtain_auth_token) ,
    path("admin/", admin.site.urls),
    
]