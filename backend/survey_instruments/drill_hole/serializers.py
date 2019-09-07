from rest_framework import  serializers
from .models import DrillHole, DepthReading


class DepthReadingSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DepthReading
        fields = ('id', 'url', 'drill_hole', 'depth', 'dip',
                  'azimuth', 'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data.pop('status')
        status = 'Untrustworthy'
        drill_hole = validated_data['drill_hole']
        depth_readings = DepthReading.objects.filter(drill_hole=drill_hole).order_by('-id')
        if (len(depth_readings) == 0):
            status = 'Trustworthy'
        else:
            # Azimuth check
            last = depth_readings[0]
            if (abs(validated_data['azimuth'] - last.azimuth) < 5.0):
                # Dip check
                last_five = depth_readings[:5]
                average_dip = sum(depth.dip for depth in last_five) / len(last_five)
                if (abs(validated_data['dip'] - average_dip) < 3.0):
                    status = 'Trustworthy'

        return DepthReading.objects.create(status=status, **validated_data)


class DrillHoleSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DrillHole
        fields = ('id', 'url', 'name', 'latitude', 'longitude',
                  'dip', 'azimuth', 'created_at', 'updated_at')
