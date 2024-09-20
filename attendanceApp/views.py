from django.shortcuts import render
from coreApp.models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status, parsers

# A ViewSet for handling CRUD operations related to Attendance.
class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        """
        return AttendanceSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all attendance records.
        """
        try:
            attendance_objs = self.get_queryset()
            serializer = self.get_serializer(attendance_objs, many=True)
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to retrieve attendance records')

    def create(self, request, *args, **kwargs):
        """
        Create a new attendance record.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'data': serializer.data,
                'message': 'Attendance added successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to add attendance record')

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve details of a specific attendance record.
        """
        try:
            attendance_obj = self.get_object()
            serializer = self.get_serializer(attendance_obj)
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to retrieve attendance record')

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update all fields of a specific attendance record.
        """
        try:
            attendance_obj = self.get_object()
            serializer = self.get_serializer(attendance_obj, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data,
                'message': 'Attendance updated successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to update attendance record')

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update specific fields of an attendance record.
        """
        try:
            attendance_obj = self.get_object()
            serializer = self.get_serializer(attendance_obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data,
                'message': 'Attendance partially updated successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to partially update attendance record')

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete a specific attendance record.
        """
        try:
            attendance_obj = self.get_object()
            attendance_obj.delete()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Attendance deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail='Failed to delete attendance record')
