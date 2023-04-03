from django.db import models

from users.models import User


class Ledger(models.Model):
    TYPE_CHOICES = [
        ("ED", "Education"),
        ("FO", "Food"),
        ("HO", "Housing"),
        ("CO", "Communication"),
        ("EN", "Entertainment"),
        ("EX", "Extra"),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    memo = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.name
