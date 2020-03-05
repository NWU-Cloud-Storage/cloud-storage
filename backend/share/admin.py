from django.contrib import admin
from .models import Share


# Register your models here.

@admin.register(Share)
class Share(admin.ModelAdmin):
    list_display = (
        'url',
        'is_unlimited',
        'expiration'
    )
