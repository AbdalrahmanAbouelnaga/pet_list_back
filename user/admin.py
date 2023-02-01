from django.contrib import admin
from .models import Profile,ProfileImage
# Register your models here.

class ImagesInline(admin.TabularInline):
    model = ProfileImage

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines =(
        ImagesInline,
    )

admin.site.register(Profile,ProfileAdmin)