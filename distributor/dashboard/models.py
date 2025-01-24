from django.db import models
from django.contrib.auth.models import AbstractUser

class Distributor(AbstractUser):
    distributor_id = models.CharField(max_length=255)
    distributor_name = models.CharField(max_length=255,unique=True) 
    USERNAME_FIELD = 'distributor_name'
    REQUIRED_FIELDS = ['distributor_id']
    
    def __str__(self):
        return f"{self.distributor_name}-{self.distributor_id}" 
    
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True,max_length=255)
    customer_name = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name

class Commission(models.Model):
    category = models.CharField(max_length=255)
    commission_percentage = models.FloatField()
    
    def __str__(self):
        return self.category
    
class Product(models.Model):
    product_id = models.CharField(primary_key=True,max_length=255)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Commission, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class Merchant(models.Model):
    merchant_id = models.CharField(primary_key=True,max_length=255)
    merchant_name = models.CharField(max_length=255)

    def __str__(self):
        return self.merchant_name

    
class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True,max_length=255)
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor,on_delete=models.CASCADE)
    commission = models.ForeignKey(Commission,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Transaction {self.transaction_id}"

