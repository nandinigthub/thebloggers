from django.contrib import admin

# Register your models here.
from .models import post,Email

admin.site.register(Email)

admin.site.register(post)