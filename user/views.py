from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions,parsers
from .models import Profile
from .serializers import ProfileSerializer,CreateProfileSerializer,ProfileListSerializer,myInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
# Create your views here.


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def myInfo(request):
    user = request.user
    serializer = myInfoSerializer(user)
    return Response(serializer.data,status=200)


class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'slug'
    parser_classes = (parsers.MultiPartParser,parsers.FormParser)

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
        data = request.data
        images = request.FILES
        print(request.FILES.getlist("images[]"))
        user_data = {
            "username":data.get("username"),
            "email":data.get("email"),
            "first_name":data.get("first_name"),
            "last_name":data.get("last_name"),
            "password":data.get("password"),
            "images":[],
        }
        serializer = CreateProfileSerializer(data=user_data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message":"Sign up successfull.Redirecting to login."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def get_object(self):
        if ((self.action == 'partial_update') | (self.action == 'destroy')):
            obj = self.queryset.get(pk=self.request.user.pk)
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()
    

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success':"user has been deleted"},status=status.HTTP_202_ACCEPTED)