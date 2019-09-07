from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('drillHole', views.DrillHoleView)
router.register('depthReading', views.DepthReadingView)

urlpatterns = [
    path('', include(router.urls)),
]