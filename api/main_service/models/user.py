from django.db import models

from .property import Property, City


class User(models.Model):
    __table__ = "users"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_of_moving_in = models.DateField(null=True, blank=True)
    pets = models.BooleanField(null=True, default=False)
    pool = models.BooleanField(null=True, default=False)
    yard = models.BooleanField(null=True, default=False)
    parking = models.BooleanField(null=True, default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    matches = models.ManyToManyField(Property, blank=True)


    def __str__(self):
        return f"{self.first_name}, email: {self.email}, phone: {self.phone}"