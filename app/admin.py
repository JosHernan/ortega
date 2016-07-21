from django.contrib import admin

from .models import Category,Casos,userProfile
# Register your models here.

admin.site.register(Category)
admin.site.register(Casos)
admin.site.register(userProfile)
