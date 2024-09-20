from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Leaveviewset

router = DefaultRouter()  
router.register('',Leaveviewset,basename='leaveApp')     
app_name = 'LeaveApp'

urlpatterns = [
    path('',include(router.urls))
]