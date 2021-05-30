from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from . import models
from . import serializers
from . permissions import IsProfileOwner
from task.models import TransportationTask, StorageTask, ShippingTask
from task.serializers import TransportationTaskSerializer, StorageTaskSerializer, ShippingTaskSerializer, TasksSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = models.UserType.objects.all()
    serializer_class = serializers.UserTypeSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    @action(detail=True, methods=["GET"])
    def user_submitter_transportation_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = TransportationTask.objects.filter(submitter=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = TransportationTask.objects.filter(submitter=models.UserProfile.objects.get(user=user))
        
        serializer = TransportationTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["GET"])
    def user_submitter_storage_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = StorageTask.objects.filter(submitter=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = StorageTask.objects.filter(submitter=models.UserProfile.objects.get(user=user))
        
        serializer = StorageTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["GET"])
    def user_submitter_shipping_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = ShippingTask.objects.filter(submitter=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = ShippingTask.objects.filter(submitter=models.UserProfile.objects.get(user=user))
        
        serializer = ShippingTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["GET"])
    def user_acceptor_transportation_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = TransportationTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = TransportationTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user))
        
        serializer = TransportationTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["GET"])
    def user_acceptor_storage_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = StorageTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = StorageTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user))
        
        serializer = StorageTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["GET"])
    def user_acceptor_shipping_tasks(self, request, pk=None):
        user = self.request.user
        
        if request.query_params and 'requested_task_status' in request.query_params:
            requested_task_status = request.query_params['requested_task_status']
        else:
            requested_task_status=''
        
        if requested_task_status:
            tasks = ShippingTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user), task_status__code=requested_task_status)
        else:
            tasks = ShippingTask.objects.filter(acceptor=models.UserProfile.objects.get(user=user))
        
        serializer = ShippingTaskSerializer(tasks, context={'request': request}, many=True)
       
        return Response(serializer.data, status=200)
    
    
class LicenceViewSet(viewsets.ModelViewSet):
    queryset = models.Licence.objects.all()
    serializer_class = serializers.LicenceSerializer


class InterestViewSet(viewsets.ModelViewSet):
    queryset = models.Interest.objects.all()
    serializer_class = serializers.InterestSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer