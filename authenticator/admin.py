from django.contrib import admin
from .models import User, Profile
# Register your models here.

class User_Admin(admin.ModelAdmin):
    list_display = ["email","age"]
    # readonly_fields = ["hero_image"]
    # prepopulated_fields = {"slug": ("Title",)}

admin.site.register(User,User_Admin)
admin.site.register(Profile)