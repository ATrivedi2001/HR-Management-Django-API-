from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Departmentviewset

router = DefaultRouter()  
router.register('',Departmentviewset,basename='departmentApp')     
app_name = 'departmentApp'

urlpatterns = [
    path('',include(router.urls))
]