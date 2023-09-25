from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags


from djoser.views import UserViewSet
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings


from . import models
from . import serializers
from .permissions import IsProfileOwner, IsSuperUser
from .serializers import SuperuserUserCreateSerializer


from task.models import TransportationTask, StorageTask, ShippingTask, TaskStatus
from task.serializers import (
    TransportationTaskSerializer,
    StorageTaskSerializer,
    ShippingTaskSerializer,
)
from vehicle.models import Vehicle
from storage.models import Storage
from notification.models import Notification
from config import settings as project_settings


class SuperUserAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserAccountSerializer

    @action(
        detail=True, methods=["PUT"], url_path="delete_user", url_name="delete_user"
    )
    def delete_user(self, request, pk=None, **kwargs):
        user = models.UserProfile.objects.get(user__id=pk, active=True)
        accepted_task_status = TaskStatus.objects.get(code="accepted")

        if user:
            transportation_tasks = TransportationTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )
            storage_tasks = StorageTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )
            shipping_tasks = ShippingTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )

            if transportation_tasks or storage_tasks or shipping_tasks:
                return Response(
                    "User can't be deleted because of tasks in progress that he submitted or accepted.",
                    status=405,
                )
            else:
                # For all user related data set active=False
                user.active = False
                user.save()

                TransportationTask.objects.filter(submitter=user).update(active=False)
                StorageTask.objects.filter(submitter=user).update(active=False)
                ShippingTask.objects.filter(submitter=user).update(active=False)
                Vehicle.objects.filter(user=user).update(active=False)
                Storage.objects.filter(user=user).update(active=False)
                Notification.objects.filter(user=user).update(active=False)
        else:
            user_account = models.User.objects.get(id=pk)
            user_account.is_active = False
            user_account.is_deleted = True
            user_account.save()

            msg = render_to_string("email/deletion.html")
            send_mail(
                "Your account has been deleted",
                strip_tags(msg),
                project_settings.EMAIL_HOST_USER,
                [user_account.email],
                html_message=msg,
                fail_silently=True,
            )

            return Response("User is successfully deleted.", status=201)

    @action(detail=True, methods=["PUT"], url_path="block_user", url_name="block_user")
    def block_user(self, request, pk=None, **kwargs):
        user = models.UserProfile.objects.get(user__id=pk, active=True)
        accepted_task_status = TaskStatus.objects.get(code="accepted")

        if user:
            transportation_tasks = TransportationTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )
            storage_tasks = StorageTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )
            shipping_tasks = ShippingTask.objects.filter(
                Q(acceptor=user) | Q(submitter=user), task_status=accepted_task_status
            )

            if transportation_tasks or storage_tasks or shipping_tasks:
                return Response(
                    "User can't be blocked because of tasks in progress that he submitted or accepted.",
                    status=405,
                )
            else:
                # For all user related data set active=False
                user.active = False
                user.save()

                TransportationTask.objects.filter(submitter=user).update(active=False)
                StorageTask.objects.filter(submitter=user).update(active=False)
                ShippingTask.objects.filter(submitter=user).update(active=False)
                Vehicle.objects.filter(user=user).update(active=False)
                Storage.objects.filter(user=user).update(active=False)
                Notification.objects.filter(user=user).update(active=False)
        else:
            user_account = models.User.objects.get(id=pk)
            user_account.is_active = False
            user_account.is_blocked = True
            user_account.save()

            msg = render_to_string("email/blockage.html")
            send_mail(
                "Your account has been blocked",
                strip_tags(msg),
                project_settings.EMAIL_HOST_USER,
                [user_account.email],
                html_message=msg,
                fail_silently=True,
            )

            return Response("User is successfully blocked.", status=201)

    @action(
        detail=True, methods=["PUT"], url_path="unblock_user", url_name="unblock_user"
    )
    def unblock_user(self, request, pk=None, **kwargs):
        user = models.UserProfile.objects.get(user__id=pk, active=False)

        if user:
            # For all user related data set active=True
            user.active = True
            user.save()

            TransportationTask.objects.filter(submitter=user).update(active=True)
            StorageTask.objects.filter(submitter=user).update(active=True)
            ShippingTask.objects.filter(submitter=user).update(active=True)
            Vehicle.objects.filter(user=user).update(active=True)
            Storage.objects.filter(user=user).update(active=True)
            Notification.objects.filter(user=user).update(active=True)

        user_account = models.User.objects.get(id=pk)
        user_account.is_active = True
        user_account.is_blocked = False
        user_account.save()

        msg = render_to_string("email/unblockage.html")
        send_mail(
            "Your account has been unblocked",
            strip_tags(msg),
            project_settings.EMAIL_HOST_USER,
            [user_account.email],
            html_message=msg,
            fail_silently=True,
        )

        return Response("User is successfully unblocked.", status=201)


class SuperuserUserCreateView(UserViewSet):
    serializer_class = SuperuserUserCreateSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            current_password = self.request.data.get("password", None)

            user_data = {"created_by_superuser": True, "password_reset_required": True}

            user_data.update(serializer.validated_data)

            user = serializer.create(user_data)

            signals.user_registered.send(
                sender=self.__class__, user=user, request=self.request
            )

            context = {"user": user, "current_password": current_password}
            to = [get_user_email(user)]
            if settings.SEND_ACTIVATION_EMAIL:
                settings.EMAIL.activation(self.request, context).send(to)
            elif settings.SEND_CONFIRMATION_EMAIL:
                settings.EMAIL.confirmation(self.request, context).send(to)
        else:
            raise PermissionDenied()


class SuperUserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = models.UserProfile.objects.filter(active=True)
    serializer_class = serializers.UserProfileSerializer


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = models.UserType.objects.filter(active=True)
    serializer_class = serializers.UserTypeSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        user = self.request.user
        return models.UserProfile.objects.filter(user=user, active=True)

    @action(detail=True, methods=["GET"])
    def user_submitter_transportation_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = TransportationTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = TransportationTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = TransportationTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user_submitter_storage_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = StorageTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = StorageTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = StorageTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user_submitter_shipping_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = ShippingTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = ShippingTask.objects.filter(
                submitter=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = ShippingTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user_acceptor_transportation_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = TransportationTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = TransportationTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = TransportationTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user_acceptor_storage_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = StorageTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = StorageTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = StorageTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user_acceptor_shipping_tasks(self, request, pk=None):
        user = self.request.user

        if request.query_params and "requested_task_status" in request.query_params:
            requested_task_status = request.query_params["requested_task_status"]
        else:
            requested_task_status = ""

        if requested_task_status:
            requested_task_status_id = TaskStatus.objects.get(
                code=requested_task_status,
            )
            tasks = ShippingTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user),
                task_status=requested_task_status_id,
                active=True,
            )
        else:
            tasks = ShippingTask.objects.filter(
                acceptor=models.UserProfile.objects.get(user=user), active=True
            )

        serializer = ShippingTaskSerializer(
            tasks, context={"request": request}, many=True
        )

        return Response(serializer.data, status=200)


class LicenceViewSet(viewsets.ModelViewSet):
    queryset = models.Licence.objects.filter(active=True)
    serializer_class = serializers.LicenceSerializer
    permission_classes = [IsAuthenticated]


class InterestViewSet(viewsets.ModelViewSet):
    queryset = models.Interest.objects.filter(active=True)
    serializer_class = serializers.InterestSerializer
    permission_classes = [IsAuthenticated]


class UserInterestsViewSet(ObjectMultipleModelAPIViewSet):
    def get_querylist(self):
        user = self.request.user
        user_interests = models.UserProfile.objects.get(
            user=user
        ).interest.through.objects.filter(active=True)

        querylist = (
            {
                "queryset": models.Interest.objects.filter(id__in=user_interests),
                "serializer_class": serializers.InterestSerializer,
                "label": "selected_interests",
            },
            {
                "queryset": models.Interest.objects.exclude(id__in=user_interests),
                "serializer_class": serializers.InterestSerializer,
                "label": "unselected_interests",
            },
        )
        return querylist
