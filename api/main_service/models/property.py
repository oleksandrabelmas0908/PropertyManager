from django.db import models

from .city import City



class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pool = models.BooleanField(null=True, default=False)
    yard = models.BooleanField(null=True, default=False)
    parking = models.BooleanField(null=True, default=False)
    pets = models.BooleanField(null=True, default=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = "properties" 
    
    def __str__(self):
        return f"{self.title} in {self.city.name} for ${self.price}"
    