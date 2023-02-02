from . import views
from user.views import ProfileViewset
from django.urls import path
from rest_framework_extensions.routers import ExtendedDefaultRouter
from rest_framework.routers import DefaultRouter

router = ExtendedDefaultRouter()
(
    router.register(r'users',ProfileViewset,basename="profile")
          .register(r'pets',views.PetViewSet,basename='profile-pets',parents_query_lookups=['owner_slug'])
)

# router = DefaultRouter()
# router.register(r'users',ProfileViewset)

# pets = NestedDefaultRouter(router,r'users',lookup='owner.slug')
# pets.register(r'pets',views.PetViewSet,basename='user-pets')

kinds = DefaultRouter()
kinds.register(r'kinds',views.KindViewset)

urlpatterns = [
    path('search/',views.search),
]+router.urls+kinds.urls