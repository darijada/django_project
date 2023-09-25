from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail

from . import models
from . import serializers

from user.models import UserProfile, User
from notification.models import Notification, NotificationMessage


class TaskStatusViewSet(viewsets.ModelViewSet):
    queryset = models.TaskStatus.objects.all()
    serializer_class = serializers.TaskStatusSerializer


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = models.TaskType.objects.all()
    serializer_class = serializers.TaskTypeSerializer


class SingleTransportationTaskViewSet(viewsets.ModelViewSet):
    queryset = models.TransportationTask.objects.filter(active=True)
    serializer_class = serializers.TransportationTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=models.TaskStatus.objects.get(code="published"))
        serializer.save(task_type=models.TaskType.objects.get(code="transportation"))

    @action(
        detail=True, methods=["PUT"], url_path="accept_task", url_name="accept_task"
    )
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()

        serializer = serializers.TransportationTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            notification_message = NotificationMessage.objects.get(code="accepted")
            Notification.objects.create(
                user=task.submitter,
                transportation_task=task,
                notification_message=notification_message,
            )
            submitter_message = render_to_string(
                "email/submitter_task_accepted.html",
                {"acceptor_email": self.request.user.email},
            )
            send_mail(
                "Your offer is accepted",
                submitter_message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=submitter_message,
                fail_silently=True,
            )

            acceptor_message = render_to_string(
                "email/acceptor_task_accepted.html",
                {"submitter_email": task.submitter.user.email},
            )
            send_mail(
                "You accepted the offer",
                acceptor_message,
                task.submitter.user.email,
                [self.request.user.email],
                html_message=acceptor_message,
                fail_silently=True,
            )

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="cancel_task", url_name="cancel_task"
    )
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="canceled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="canceled_acceptor")

        serializer = serializers.TransportationTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            notification_message = NotificationMessage.objects.get(code="canceled")
            Notification.objects.create(
                user=task.submitter,
                transportation_task=task,
                notification_message=notification_message,
            )
            message = render_to_string("email/task_canceled.html")
            send_mail(
                "Your offer is canceled",
                message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=message,
                fail_silently=True,
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="complete_task", url_name="complete_task"
    )
    def complete_task(self, request, pk=None, **kwargs):
        task = self.get_object()
        task_status = models.TaskStatus.objects.get(code="completed")

        serializer = serializers.TransportationTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class TransportationTasksViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransportationTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if (
            self.request.query_params
            and "requested_task_status" in self.request.query_params
        ):
            requested_task_status = self.request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = models.TaskStatus.objects.filter(
                code=requested_task_status,
            )
            queryset = models.TransportationTask.objects.filter(
                task_status=requested_task_status_id[0].id, active=True
            )
        else:
            queryset = models.TransportationTask.objects.filter(active=True)

        return queryset.exclude(submitter=UserProfile.objects.get(user=user))


class SingleStorageTaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StorageTaskSerializer
    queryset = models.StorageTask.objects.filter(active=True)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=models.TaskStatus.objects.get(code="published"))
        serializer.save(task_type=models.TaskType.objects.get(code="storage"))

    @action(
        detail=True, methods=["PUT"], url_path="accept_task", url_name="accept_task"
    )
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()

        serializer = serializers.StorageTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            notification_message = NotificationMessage.objects.get(code="accepted")
            Notification.objects.create(
                user=task.submitter,
                storage_task=task,
                notification_message=notification_message,
            )
            submitter_message = render_to_string(
                "email/submitter_task_accepted.html",
                {"acceptor_email": self.request.user.email},
            )
            send_mail(
                "Your offer is accepted",
                submitter_message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=submitter_message,
                fail_silently=True,
            )

            acceptor_message = render_to_string(
                "email/acceptor_task_accepted.html",
                {"submitter_email": task.submitter.user.email},
            )
            send_mail(
                "You accepted the offer",
                acceptor_message,
                task.submitter.user.email,
                [self.request.user.email],
                html_message=acceptor_message,
                fail_silently=True,
            )

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="cancel_task", url_name="cancel_task"
    )
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="canceled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="canceled_acceptor")

        serializer = serializers.StorageTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            notification_message = NotificationMessage.objects.get(code="canceled")
            Notification.objects.create(
                user=task.submitter,
                storage_task=task,
                notification_message=notification_message,
            )
            message = render_to_string("email/task_canceled.html")
            send_mail(
                "Your offer is canceled",
                message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=message,
                fail_silently=True,
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="complete_task", url_name="complete_task"
    )
    def complete_task(self, request, pk=None, **kwargs):
        task = self.get_object()
        task_status = models.TaskStatus.objects.get(code="completed")

        serializer = serializers.StorageTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class StorageTasksViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StorageTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if (
            self.request.query_params
            and "requested_task_status" in self.request.query_params
        ):
            requested_task_status = self.request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = models.TaskStatus.objects.filter(
                code=requested_task_status,
            )
            queryset = models.StorageTask.objects.filter(
                task_status=requested_task_status_id[0].id, active=True
            )
        else:
            queryset = models.StorageTask.objects.filter(active=True)

        return queryset.exclude(submitter=UserProfile.objects.get(user=user))


class SingleShippingTaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShippingTaskSerializer
    queryset = models.ShippingTask.objects.filter(active=True)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(submitter=UserProfile.objects.get(user=user))
        serializer.save(task_status=models.TaskStatus.objects.get(code="published"))
        serializer.save(task_type=models.TaskType.objects.get(code="shipping"))

    @action(
        detail=True, methods=["PUT"], url_path="accept_task", url_name="accept_task"
    )
    def accept_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task_status = models.TaskStatus.objects.get(code="accepted")
        task = self.get_object()

        serializer = serializers.ShippingTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status, acceptor=user)
            notification_message = NotificationMessage.objects.get(code="accepted")
            Notification.objects.create(
                user=task.submitter,
                shipping_task=task,
                notification_message=notification_message,
            )
            submitter_message = render_to_string(
                "email/submitter_task_accepted.html",
                {"acceptor_email": self.request.user.email},
            )
            send_mail(
                "Your offer is accepted",
                submitter_message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=submitter_message,
                fail_silently=True,
            )

            acceptor_message = render_to_string(
                "email/acceptor_task_accepted.html",
                {"submitter_email": task.submitter.user.email},
            )
            send_mail(
                "You accepted the offer",
                acceptor_message,
                task.submitter.user.email,
                [self.request.user.email],
                html_message=acceptor_message,
                fail_silently=True,
            )

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="cancel_task", url_name="cancel_task"
    )
    def cancel_task(self, request, pk=None, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        task = self.get_object()

        if task.submitter == user:
            task_status = models.TaskStatus.objects.get(code="canceled_submitter")
        else:
            task_status = models.TaskStatus.objects.get(code="canceled_acceptor")
        serializer = serializers.ShippingTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status)
            notification_message = NotificationMessage.objects.get(code="canceled")
            Notification.objects.create(
                user=task.submitter,
                shipping_task=task,
                notification_message=notification_message,
            )
            message = render_to_string("email/task_canceled.html")
            send_mail(
                "Your offer is canceled",
                message,
                self.request.user.email,
                [task.submitter.user.email],
                html_message=message,
                fail_silently=True,
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(
        detail=True, methods=["PUT"], url_path="complete_task", url_name="complete_task"
    )
    def complete_task(self, request, pk=None, **kwargs):
        task = self.get_object()
        task_status = models.TaskStatus.objects.get(code="completed")

        serializer = serializers.ShippingTaskSerializer(
            task, data=request.data, context={"request": request}, partial=True
        )

        if serializer.is_valid():
            serializer.save(task_status=task_status)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ShippingTasksViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShippingTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if (
            self.request.query_params
            and "requested_task_status" in self.request.query_params
        ):
            requested_task_status = self.request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            if requested_task_status:
                requested_task_status_id = models.TaskStatus.objects.filter(
                    code=requested_task_status,
                )
                queryset = models.ShippingTask.objects.filter(
                    task_status=requested_task_status_id[0].id, active=True
                )
        else:
            queryset = models.ShippingTask.objects.filter(active=True)

        return queryset.exclude(submitter=UserProfile.objects.get(user=user))
