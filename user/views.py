from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Profile
from .serializers import ProfileSerializer,CreateProfileSerializer,ProfileListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
import ujson




@api_view(['POST'])
def sign_up(request):
    req_data =ujson.loads(request.data.get("data")) 
    data = {
        "username": req_data["username"],
        "email": req_data["email"],
        "last_name": req_data["last_name"],
        "first_name": req_data["first_name"],
        "password": req_data["password"],
        "images":[]
    }

    serializer = CreateProfileSerializer(data=data,context = {"request":request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"success"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=500)    





class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        if ((self.action == 'update') | (self.action == 'destroy')):
            return [permissions.IsAuthenticated(),]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProfileSerializer
        if self.action == 'list':
            return ProfileListSerializer
        return ProfileSerializer
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context.update({'request':self.request})
        return context

    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'New User Created.'}, status=201)
    

    def get_object(self):
        if ((self.action == 'partial_update') | (self.action == 'destroy')):
            obj = self.queryset.get(pk=self.request.user.pk)
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()
    

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success':"user has been deleted"},status=status.HTTP_202_ACCEPTED)