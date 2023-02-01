from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import status
from .models import Pet,Kind,Breed,PetImage
from .serializers import PetSerializer,PetDetailSerializer,KindSerializer,BreedSerializer
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework import parsers
import ujson
from django.db.models import Q

from user.models import Profile
from user.serializers import ProfileListSerializer

@api_view(['POST'])
def search(request):
    query = request.data.get('query','')
    
    pets = Pet.objects.filter(Q(name__icontains=query))
    pets_serializer = PetSerializer(pets,many=True,context={'request':request})
    users = Profile.objects.filter(Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query))
    users_serializer = ProfileListSerializer(users,many=True,context={'request':request})
    return Response({
        "users":users_serializer.data,
        "pets":pets_serializer.data
    },status=200)









@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def myPetsView(request):
    data = Pet.objects.filter(owner = request.user.pk)
    serializer = PetSerializer(data,many=True,context={'request': request})
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
@parser_classes([parsers.MultiPartParser,parsers.FormParser])
def addPet(request):
    req_data =ujson.loads(request.data.get("data"))
    print(req_data["breed"])
    data = {
        "name": req_data["name"],
        "birth_date":req_data["birth_date"],
        "breed":req_data["breed"],
        "images":request.FILES,
    }
    print(data)

    serializer = PetDetailSerializer(data=data,context = {"request":request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"success"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=500)
    



class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    lookup_field = 'slug'
    def get_serializer_class(self, *args, **kwargs):
        if self.action =='create' or self.action == 'partial_update':
            return PetDetailSerializer
        return PetSerializer
    
    def get_permissions(self):
        if self.action == 'create' or self.action =='partial_update':
            return [permissions.IsAuthenticated(),]
        return super().get_permissions()



class KindViewset(ModelViewSet):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action =='destroy' or self.action == 'update':
            return [permissions.IsAuthenticated(),]
        return super().get_permissions()