from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Profile,ProfileImage
from django.urls import reverse
from pet.serializers import PetSerializer


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()


    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image.url:
            return request.build_absolute_uri(f'{obj.image.url}')
        return ''

    def get_thumbnail(self,obj):
        request = self.context.get('request')
        if obj.thumbnail.url:
            return request.build_absolute_uri(f'{obj.thumbnail.url}')
        return ''

    class Meta:
        model = ProfileImage
        fields = [
            'image',
            'thumbnail'
        ]


class CreateProfileImageSerializer(serializers.ModelSerializer):
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
        model = ProfileImage
        fields = (
            'image',
            'thumbnail'
        )

class CreateProfileSerializer(serializers.ModelSerializer):
    images = CreateProfileImageSerializer(many=True)
    class Meta:
        model = Profile
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'images',
        )
    def create(self, validated_data):
        request = self.context["request"]
        validated_data.pop('images')
        password = validated_data.pop('password')
        prof = Profile(**validated_data)
        prof.set_password(password)
        prof.save()
        images = []
        for image in request.FILES:
            images.append(request.FILES[image])
        for image in images:
            print(image)
            img = ProfileImage(profile=prof,image=image)
            img.save()
        
        return prof


class ProfileSerializer(WritableNestedModelSerializer):
    images = ProfileImageSerializer(many=True)
    url = serializers.SerializerMethodField()
    pets = PetSerializer(many=True)
    def get_url(self,obj):
        return reverse('profile-detail',kwargs={'slug':obj.slug})
    class Meta:
        model = Profile
        fields = (
            'url',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'images',
            'pets',
        )
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ProfileListSerializer(serializers.ModelSerializer):
    images = ProfileImageSerializer(many=True)
    url = serializers.SerializerMethodField()

    def get_url(self,obj):
        return reverse('profile-detail',kwargs={'slug':obj.slug})

    class Meta:
        model = Profile
        fields = (
            'url',
            'username',
            'images',
        )