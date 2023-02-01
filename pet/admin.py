from django.contrib import admin
from .models import PetImage,Pet,Kind,Breed
# Register your models here.


class ImageInline(admin.TabularInline):
    model = PetImage



class PetAdmin(admin.ModelAdmin):
    model = Pet
    inlines =(
        ImageInline,
    )

admin.site.register(Pet,PetAdmin)

admin.site.register(Kind)
admin.site.register(Breed)