from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'user_types', views.UserTypeViewSet)
router.register(r'user_licences', views.LicenceViewSet)
router.register(r'user_interests', views.InterestViewSet)
router.register(r'user_notifications', views.NotificationViewSet)