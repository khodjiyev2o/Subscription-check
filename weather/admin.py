from django.contrib import admin
from .models import Client, BankAccount, Subscription, City
# Register your models here.

admin.site.register(Client)
admin.site.register(BankAccount)
admin.site.register(Subscription)
admin.site.register(City)