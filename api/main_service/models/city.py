from django.db import models


class City(models.Model):
    __table__ = "cities"

    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"