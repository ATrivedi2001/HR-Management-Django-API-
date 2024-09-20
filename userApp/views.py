from django.shortcuts import render
from .serializers import Userserializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from coreApp.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

# @extend_schema(auth=[])
class RegisterUserAPIView(APIView):
    """Create User for authentication."""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
   

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        query_serializer=RegisterSerializer,
        security=[],
    )
    def post(self, request):
        """Get request data & save."""
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'errors':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response({
            'status':status.HTTP_201_CREATED,
            # 'data':serializer.data,
            'message':'User added successfully'
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage user profile.
    """
    serializer_class = Userserializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    
    def get(self, *args):
        """
        Retrieve user details.
        """
        user_obj = self.get_object()
        serializer = Userserializer(user_obj)

        return Response(({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        }))

  
    def patch(self, request):
        """
        Partially update user details.
        """
        user_obj = self.get_object()
        serializer = Userserializer(user_obj,data=request.data,partial=True)

        if not serializer.is_valid():
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'error':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response(({
            'status':status.HTTP_200_OK,
            'message':'User partially updated successfully'
        }))

    
    def put(self, request):
        """
        Update user details.
        """
        user_obj = self.get_object()
        serializer = Userserializer(user_obj,data=request.data,partial=False)

        if not serializer.is_valid():
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'error':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response(({
            'status':status.HTTP_200_OK,
            'message':'User updated successfully'
         }))
    
#------------user view set---------------------------------# 
class UserViewSet(ModelViewSet):
    """
    ViewSet for handling user instances.
    """
    queryset = User.objects.all()
    serializer_class=Userserializer


    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'list':
            return Userserializer
        elif self.action == 'create':
            return Userserializer
        return self.serializer_class
    
    def list(self,request):
        """
        Handle GET requests for retrieving all users.
        """
        try:
            User_objs = User.objects.all()
            serializer = self.get_serializer(User_objs, many = True)

            return Response({
                'status':status.HTTP_200_OK,
                'data': serializer.data
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })
        
    def create(self,request):
        """
         Handle POST requests for creating a new user.
        """
        try:
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'data': serializer.errors,
                    'message':'Invalid data'
                })
            serializer.save()

            return Response({
                'status':status.HTTP_201_CREATED,
                'data': serializer.data,
                'messaage':'User added successfully'
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })

    def retrieve(self,request,pk=None):
        """
        Handle GET requests for retrieving a single user.
        """
        try:
            id = pk
            if id is not None:
                User_objs = self.get_object()
                serializer = self.get_serializer(User_objs)

            return Response({
                'status':status.HTTP_200_OK,
                'data': serializer.data
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })

    def update(self,request, pk=None):
        """
        Handle PUT requests for updating all fields of a user.
        """
        try:
            User_objs = self.get_object()
            serializer = self.get_serializer(User_objs,data=request.data, partial=False)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'data': serializer.errors,
                    'message':'Invalid data'
                })
            serializer.save()

            return Response({
                'status':status.HTTP_200_OK,
                'data': serializer.data,
                'messaage':'User updated successfully'
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })
        

    def partial_update(self,request, pk=None):
        """
        Handle PATCH requests for updating specific fields of a user.
        """
        try:
            User_objs = self.get_object()
            serializer = self.get_serializer(User_objs,data=request.data,partial = True)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'data': serializer.errors,
                    'message':'Invalid data'
                })
            serializer.save()

            return Response({
                'status':status.HTTP_200_OK,
                'data': serializer.data,
                'messaage':'User updated successfully'
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })

    def destroy(self, request,pk):
        """
        Handle DELETE requests for deleting a specific user.
        """
        try:
            id=pk
            User_objs = self.get_object()
            User_objs.delete()
            return Response({
                'status':status.HTTP_200_OK,
                'messaage':'User deleted successfully'
            })

        except Exception as e:
            print(e)
            raise APIException({
                'message':APIException.default_detail,
                'status': APIException.status_code
            })
        