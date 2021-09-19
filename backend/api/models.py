from django.db import models

# Create your models here.
class Doctor(models.Model):
    user_id = models.CharField(verbose_name="ID врача", max_length=20)
    username = models.CharField(verbose_name="Имя врача", max_length=50)
    specialization = models.CharField(verbose_name="Специализация", max_length=60)

    def __str__(self) -> str:
        return self.specialization + " " + self.username

class Order(models.Model):
    user_id = models.CharField(verbose_name="ID пользователя", max_length=20, default="1")
    order_id = models.CharField(verbose_name="ID заявки", max_length=100)
    description = models.TextField(verbose_name="Описание")
    phone = models.CharField(verbose_name="Номер", default="", max_length=20)
    address = models.CharField(verbose_name="Адрес", max_length=100)
    # doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.CASCADE, default="0")
    is_accept = models.BooleanField(verbose_name="Найден врач", default="False")
    is_ready = models.BooleanField(verbose_name="Выполнена", default="False")

    def __str__(self) -> str:
        return self.order_id[:5] 

# class Order(models.Model):
#     name = "Order"

# class Order(models.Model):
#     name = "Order"