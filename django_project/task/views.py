from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import UserProfile
from user.serializers import UserProfileSerializer
from vehicle.serializers import VehicleSerializer
from . import models
from . import serializers
from collections import namedtuple
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet


class CargoTypeViewSet(viewsets.ModelViewSet):
    queryset = models.CargoType.objects.all()
    serializer_class = serializers.CargoTypeSerializer


class TaskStatusViewSet(viewsets.ModelViewSet):
    queryset = models.TaskStatus.objects.all()
    serializer_class = serializers.TaskStatusSerializer


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = models.TaskType.objects.all()
    serializer_class = serializers.TaskTypeSerializer


class TransportationTaskViewSet(viewsets.ModelViewSet):
    queryset = models.TransportationTask.objects.all()
    serializer_class = serializers.TransportationTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=TaskStatus.objects.get(code="published"))
    
    @action(detail=True, methods=["PUT"], url_path='accept_task', url_name='accept_task')
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()
        
        serializer = serializers.TransportationTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=["PUT"], url_path='cancel_task', url_name='cancel_task')
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="cancelled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="cancelled_accepter")
        
        serializer = serializers.TransportationTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class StorageTaskViewSet(viewsets.ModelViewSet):
    queryset = models.StorageTask.objects.all()
    serializer_class = serializers.StorageTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=TaskStatus.objects.get(code="published"))
    
    @action(detail=True, methods=["PUT"], url_path='accept_task', url_name='accept_task')
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()
        
        serializer = serializers.StorageTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["PUT"], url_path='cancel_task', url_name='cancel_task')
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="cancelled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="cancelled_accepter")
        
        serializer = serializers.StorageTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ShippingTaskViewSet(viewsets.ModelViewSet):
    queryset = models.ShippingTask.objects.all()
    serializer_class = serializers.ShippingTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=TaskStatus.objects.get(code="published"))
    
    @action(detail=True, methods=["PUT"], url_path='accept_task', url_name='accept_task')
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()
        
        serializer = serializers.ShippingTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["PUT"], url_path='cancel_task', url_name='cancel_task')
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="cancelled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="cancelled_accepter")
        
        serializer = serializers.ShippingTaskSerializer(task, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MarketTasksViewSet(ObjectMultipleModelAPIViewSet):
    def get_querylist(self):
        if self.request.query_params and 'requested_task_status' in self.request.query_params:
            requested_task_status = self.request.query_params['requested_task_status']

            querylist = (
                {'queryset': models.TransportationTask.objects.filter(task_status__code=requested_task_status), 'serializer_class': serializers.TransportationTaskSerializer, 'label': 'transportation_tasks'},
                {'queryset': models.StorageTask.objects.filter(task_status__code=requested_task_status), 'serializer_class': serializers.StorageTaskSerializer, 'label': 'storage_tasks'},
                {'queryset': models.ShippingTask.objects.filter(task_status__code=requested_task_status), 'serializer_class': serializers.ShippingTaskSerializer, 'label': 'shipping_tasks'},
            )
        else:
            querylist = (
                {'queryset': models.TransportationTask.objects.all(), 'serializer_class': serializers.TransportationTaskSerializer, 'label': 'transportation_tasks'},
                {'queryset': models.StorageTask.objects.all(), 'serializer_class': serializers.StorageTaskSerializer, 'label': 'storage_tasks'},
                {'queryset': models.ShippingTask.objects.all(), 'serializer_class': serializers.ShippingTaskSerializer, 'label': 'shipping_tasks'},
            )
        return querylist