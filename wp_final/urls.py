"""wp_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from th2928_final import views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.home, name="home"),
    path('home',views.home, name='home1'),
    path('maintenance',views.maintenance,name='maintenance'),
    path('cities',views.view_cities, name='cities'),
    path('weather',views.view_weather, name='weather'),
    path("assignment2", views.assignment2, name="assignment2"),
    path('register',views.register_new_user,name="register_user"),
    path('estimate',views.estimate,name="estimate"),
    path('journey',views.journey,name="journey"),
    path('end',views.end,name="end"),

]
