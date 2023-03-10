from django.db import models
from django.contrib.auth.models import AbstractUser
from io import BytesIO
from PIL import Image
from django.core.files import File
from uuid import uuid4
from django_extensions.db.fields import AutoSlugField
# Create your models here.


class Profile(AbstractUser):
    id = models.UUIDField(default=uuid4,unique=True,editable=False,primary_key=True)
    slug = AutoSlugField(populate_from=['username','first_name','last_name'])



def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class ProfileImage(models.Model):
    id = models.UUIDField(default=uuid4,unique=True,editable=False,primary_key=True)
    profile = models.ForeignKey(Profile,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to,null=True,blank=True)
    thumbnail = models.ImageField(upload_to=upload_to,null=True,blank=True)


    def make_thumbnail(self):
        img = Image.open(self.image)
        img.convert('RGB')

        aspect_ratio = img.width /img.height
        size=(aspect_ratio*400,400)

        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=100)

        thumbnail = File(thumb_io,name=self.image.name)
        self.thumbnail = thumbnail
    def save(self) -> None:
        self.make_thumbnail()
        return super().save()