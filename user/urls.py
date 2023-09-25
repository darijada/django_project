from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(
    r"su_create_account", views.SuperuserUserCreateView, basename="Create User Account"
)
router.register(r"su_accounts", views.SuperUserAccountViewSet, basename="User Account")
router.register(r"su_profiles", views.SuperUserProfileViewSet, basename="User Profiles")
router.register(r"profiles", views.UserProfileViewSet, basename="User Profile")
router.register(r"user_types", views.UserTypeViewSet)
router.register(r"user_licences", views.LicenceViewSet)
router.register(r"interests", views.InterestViewSet)
router.register(
    r"user_interests", views.UserInterestsViewSet, basename="user_interests"
)
