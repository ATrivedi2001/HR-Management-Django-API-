from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

router = DefaultRouter()  
router.register('',AttendanceViewSet,basename='attendanceApp')     
app_name = 'attendanceApp'

urlpatterns = [
    path('',include(router.urls))
]