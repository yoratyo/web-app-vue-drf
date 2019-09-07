from django.db import models


class DrillHole(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    dip = models.FloatField()
    azimuth = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DepthReading(models.Model):
    drill_hole = models.ForeignKey(DrillHole, related_name='DepthReadings', on_delete=models.CASCADE)
    depth = models.FloatField()
    dip = models.FloatField()
    azimuth = models.FloatField()
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.drill_hole.name, str(self.depth))

    class Meta:
        ordering = ['-id']