from rest_framework import serializers

from fish_tanks.models import *


class FishTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishTank
        fields = '__all__'
