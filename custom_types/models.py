from django.db import models

from users.models import User


class CustomType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "user"]

    def __str__(self):
        return self.name
