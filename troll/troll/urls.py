"""troll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from trollapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login_user', views.login_user, name="login"),
    # path('moderate/', views.moderate, name="moderate"),
    path('', views.index, name="index"),
    path('reports/', views.report, name="reports"),
    path('logout/', views.logout_user, name="logout"),
    path('base/', views.base, name="base"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
