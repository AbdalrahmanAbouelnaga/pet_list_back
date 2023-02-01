from django.db import models
from uuid import uuid4
from PIL import Image
from io import BytesIO
from django.core.files import File
from django_extensions.db.fields import AutoSlugField
from user.models import Profile


class Kind(models.Model):
    id = models.UUIDField(default=uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=['name'])

    def __str__(self):
        return self.name
    

class Breed(models.Model):
    id = models.UUIDField(default=uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(Kind,on_delete=models.CASCADE,related_name='breeds')
    slug = AutoSlugField(populate_from=['name'])

    def __str__(self):
        return self.name


class Pet(models.Model):
    id = models.UUIDField(default=uuid4,editable=False,primary_key=True,unique=True)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='pets')
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from=['name',])
    breed = models.ForeignKey(Breed,on_delete=models.CASCADE,related_name='pets',null=True)
    birth_date = models.DateField()
    def __str__(self):
        return self.name







class PetImage(models.Model):
    id = models.UUIDField(default=uuid4,unique=True,editable=False,primary_key=True)
    pet = models.ForeignKey(Pet,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True)
    thumbnail = models.ImageField(blank=True,null=True)


    def make_thumbnail(self):
        img = Image.open(self.image)
        img.convert('RGB')
        aspect_ratio = img.width /img.height
        size = (aspect_ratio*200,200)

        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=100)

        thumbnail = File(thumb_io,name=self.image.name)
        self.thumbnail = thumbnail
    def save(self) -> None:
        self.make_thumbnail()
        return super().save()