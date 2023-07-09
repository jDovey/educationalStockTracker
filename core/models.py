from django.db import models

from user.models import Student

# Create your models here.
class Transactions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ['-date']

    def __str__(self):
        return self.symbol
    
class Holdings(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Holdings"
        ordering = ['symbol']
    
    def __str__(self):
        return f'{self.quantity} | {self.symbol} (${self.purchase_price})'