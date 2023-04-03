from django.db import models

from custom_types.models import CustomType
from users.models import User


class Ledger(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    memo = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(CustomType, on_delete=models.PROTECT)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Ledgers"
        ordering = ["-date", "-id"]

    def __str__(self):
        return self.name
