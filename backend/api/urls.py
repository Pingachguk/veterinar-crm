from django.urls import path, include
from .views import DoctorViewSet, hello, OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'doctors', DoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("hello/", hello)
]