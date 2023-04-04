from django.db import models

from users.models import User


class CustomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["name", "user"]
        ordering = ["name"]

    def __str__(self):
        return self.name
