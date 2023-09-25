from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r"currency", views.CurrencyViewSet)
router.register(r"country", views.CountryViewSet)
router.register(r"city", views.CityViewSet)
router.register(r"language", views.LanguageViewSet)
