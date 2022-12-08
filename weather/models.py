from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)
    

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = 'clients'


    def add_client(sender,instance,created,**kwargs):
        user = instance
        if created:
                Client.objects.create(user=user,date_joined=datetime.date.today())

class BankAccount(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=150, null=False, blank=False)
    card_number = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.client.user.username)
    
    class Meta:
        verbose_name_plural = 'bankaccounts'


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.client.user.username)

    class Meta:
        verbose_name_plural = 'subscriptions'

    def add_5day_subscription(sender,instance,created,**kwargs):
        client = instance
        t_delta = datetime.timedelta(days=25)
        today = datetime.date.today()
        date_paid = today - t_delta
        if created:
                Subscription.objects.create(client=client,date_paid=date_paid)



class City(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'


post_save.connect(Client.add_client,sender=User)
post_save.connect(Subscription.add_5day_subscription,sender=Client)