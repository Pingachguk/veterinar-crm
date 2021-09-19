from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Order, Doctor
from .serializers import OrderSerializer, DoctorSerializer
from rest_framework import filters


# Create your views here.
def hello(request):
    return HttpResponse("Hello")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_id']