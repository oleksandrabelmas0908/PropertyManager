from django.contrib import admin
from .models import User, Property, City


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "first_name",
        "last_name",
        "bedrooms",
        "max_budget",
        "monthly_income",
        "city",
    )
    search_fields = ("email", "phone", "first_name", "last_name")
    list_filter = ("city",)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "price")
    search_fields = ("title", "description", "city__name")
    list_filter = ("city",)


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    search_fields = ("name", "country",)


admin.site.register(User, UserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(City, CityAdmin)