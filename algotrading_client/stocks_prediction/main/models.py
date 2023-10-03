from django.db import models

# Create your models here.
#class Stock(models.Model):
#    name = models.CharField(max_length=100)
#    price_tomorrow = models.DecimalField(max_digits=100, decimal_places=3)

#    def __str__(self):
#        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=100)
    today_price = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    mse = models.DecimalField(max_digits=10, decimal_places=2)