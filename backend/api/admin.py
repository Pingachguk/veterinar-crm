from django.contrib import admin
from .models import Order, Doctor

# Register your models here.
admin.site.register(Order)
admin.site.register(Doctor)