from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "cities"

    def __str__(self):
        return f"{self.name}, {self.country}"