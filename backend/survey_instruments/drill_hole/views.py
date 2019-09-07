from rest_framework import viewsets
from .models import DrillHole, DepthReading
from .serializers import DrillHoleSerializers, DepthReadingSerializers


class DrillHoleView(viewsets.ModelViewSet):
    queryset = DrillHole.objects.all()
    serializer_class = DrillHoleSerializers


class DepthReadingView(viewsets.ModelViewSet):
    queryset = DepthReading.objects.all()
    serializer_class = DepthReadingSerializers
    filterset_fields = ['drill_hole']
