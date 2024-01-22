from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from projects.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    total_dead = serializers.IntegerField(read_only=True, default=0)
    total_live = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        from fish_tanks.api.v1.serializers import FishTankSerializer

        if instance.tank:
            res['tank'] = FishTankSerializer(instance.tank).data
        else:
            res['tank'] = None
        return res
