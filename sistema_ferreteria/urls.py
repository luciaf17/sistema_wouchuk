"""
URL configuration for sistema_ferreteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from clientes.views import home



urlpatterns = [
    path("admin/", admin.site.urls),

    path('clientes/', include('clientes.urls')),  # Incluye las URLs de la app "clientes"

    path('stock/', include('stock.urls')),

    path('productos/', include('productos.urls')),

    path('remitos/', include('remitos.urls')),

    # URL para el login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # URL para el logout
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('', home, name='home'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),


]
