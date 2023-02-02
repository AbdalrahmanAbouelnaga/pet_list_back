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
    image = serializers.ImageField(required=False)
    profile = serializers.ReadOnlyField(source='profile.id')
    class Meta:
        model = ProfileImage
        fields = (
            'profile',
            'image',
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

    def create(self,validated_data):
        print(validated_data)
        validated_data.pop("images")
        images = self.context["request"].FILES.getlist("images[]")
        password = validated_data.pop("password")
        instance = Profile(**validated_data)
        instance.set_password(password)
        instance.save()
        for image in images:
            img = ProfileImage(profile=instance,image=image)
            print(img)
            img.save()
        return instance
        


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


class myInfoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self,obj):
        return reverse('profile-detail',kwargs={'slug':obj.slug})

    class Meta:
        model = Profile
        fields = (
            'url',
            'username',
        )