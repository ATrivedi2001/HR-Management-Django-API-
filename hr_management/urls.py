"""HRManagement URL Configuration

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
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="HR Management API",
      default_version='v1',
      description="About HR Management",
      terms_of_service="https://127.0.0.1:800/",
      contact=openapi.Contact(email="trivediakshay2001@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
    name='schema-swagger-ui'),
    path('api/leave/',include('leaveApp.urls')),
    path('api/attendance/',include('attendanceApp.urls')),
    path('api/User/',include('userApp.urls')),
    path('api/Department/',include('departmentApp.urls')),
    path('api/Applicant/',include('applicantApp.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)