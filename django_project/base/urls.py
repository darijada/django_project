from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'currency', views.CurrencyViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'language', views.LanguageViewSet)