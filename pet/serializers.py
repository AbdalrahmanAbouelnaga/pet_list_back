from rest_framework import serializers
from .models import Pet,PetImage,Kind,Breed
from drf_writable_nested import WritableNestedModelSerializer
from datetime import date,timedelta
import time 
from django.urls import reverse


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = (
            'id',
            'name',
            'slug'
        )


class KindSerializer(serializers.ModelSerializer):
    breeds = BreedSerializer(many=True)
    class Meta:
        model = Kind
        fields = (
            'id',
            'name',
            'slug',
            'breeds'
        )




class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()


    def get_image(self,obj):
        request = self.context.get('request')
        if  obj.image.url:
            return request.build_absolute_uri(f'{obj.image.url}')
        else:
            return ''
        
    def get_thumbnail(self,obj):
        request = self.context.get('request')
        if  obj.thumbnail.url:
            return request.build_absolute_uri(f'{obj.thumbnail.url}')
        else:
            return ''

    class Meta:
        model = PetImage
        fields = (
            'image',
            'thumbnail'
        )


class CreatePetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)


    class Meta:
        model = PetImage
        fields = (
            'image',
        )


class PetSerializer(WritableNestedModelSerializer):
    images = PetImageSerializer(many=True)
    age = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_owner(self,obj):
        return {
            'url':reverse('profile-detail',kwargs={'slug':obj.owner.slug}),
            'name':obj.owner.username
        }

    def get_kind(self,obj):
        return obj.breed.kind.name

    def get_breed(self,obj):
        return obj.breed.name

    def get_url(self,obj):
        return reverse('user-pets-detail',kwargs={
            'owner_slug':obj.owner.slug,
            'slug':obj.slug
        })

    def get_age(self,obj):
        birthdate = obj.birth_date
        today = date.today()
        if today.year-birthdate.year <2:
            td =  today-birthdate
            format='%m-%d'
            time_obj = time.gmtime(td.total_seconds())
            return f'{time_obj.tm_mon-1} months, {time_obj.tm_mday-1} days'
        else:
            return today.year-birthdate.year

    class Meta:
        model = Pet
        fields = (
            'url',
            'id',
            'owner',
            'name',
            'kind',
            'breed',
            'birth_date',
            'age',
            'images'
        )



class PetDetailSerializer(WritableNestedModelSerializer):
    images = PetImageSerializer(many=True)
    breed = serializers.SlugRelatedField(slug_field='name',read_only=True)

    class Meta:
        model = Pet
        fields = (
            'id',
            'name',
            'breed',
            'birth_date',
            'images'
        )
    
    
    def create(self,validated_data):
        print(validated_data)
        breed_name = self.context["request"].data["breed"]
        try:
            breed = Breed.objects.get(name=breed_name)
        except Breed.DoesNotExist:
            kind_name = self.context["request"].data["kind"]
            try:
                kind = Kind.objects.get(name=kind_name)
                breed = Breed(kind=kind,name=breed_name)
                breed.save()
            except Kind.DoesNotExist:
                kind = Kind(name=kind_name)
                kind.save()
                breed = Breed(kind=kind,name=breed_name)
                breed.save()
        validated_data.pop("images")
        images = self.context["request"].FILES.getlist("images[]")
        instance = Pet(owner=self.context["request"].user,breed=breed,**validated_data)
        instance.save()
        for image in images:
            img = PetImage(pet=instance,image=image)
            img.save()
        return instance
        