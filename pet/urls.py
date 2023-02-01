from . import views
from user.views import ProfileViewset
from django.urls import path

from rest_framework_nested.routers import DefaultRouter,NestedDefaultRouter


router = DefaultRouter()
router.register(r'users',ProfileViewset)

pets = NestedDefaultRouter(router,r'users',lookup='owner')
pets.register(r'pets',views.PetViewSet,basename='user-pets')

kinds = DefaultRouter()
kinds.register(r'kinds',views.KindViewset)

urlpatterns = [
    path('search/',views.search),
    path('mypets/',views.myPetsView),
    path('add-pet/',views.addPet),
]+router.urls+pets.urls+kinds.urls