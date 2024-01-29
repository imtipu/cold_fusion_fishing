from rest_framework import serializers

from fish_tanks.models import *
from projects.api.v1.serializers import ProjectSerializer


class FishTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishTank
        fields = '__all__'


class FishTankListSerializer(serializers.ModelSerializer):
    total_dead = serializers.IntegerField(default=0, read_only=True)
    total_live = serializers.IntegerField(default=0, read_only=True)
    current_project = ProjectSerializer(read_only=True)

    class Meta:
        model = FishTank
        fields = '__all__'


class FishTankDetailSerializer(serializers.ModelSerializer):
    total_dead = serializers.IntegerField(default=0, read_only=True)
    total_live = serializers.IntegerField(default=0, read_only=True)
    current_project = ProjectSerializer(read_only=True)

    class Meta:
        model = FishTank
        fields = '__all__'
        # extra_kwargs = {
        #     'current_project': {'read_only': True},
        # }


class FishTankUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishTank
        fields = '__all__'

    def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        res['current_project'] = ProjectSerializer(instance.current_project).data
        return res
