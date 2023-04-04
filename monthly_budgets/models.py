from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class MonthlyBudget(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    budget = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ("user", "year", "month")
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.year}-{self.month} Budget for user {self.user.id}"
