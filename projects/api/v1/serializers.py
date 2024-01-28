from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from projects.models import *
from projects.utils import calculate_feed_n, calculate_feed_c


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'title': {
                'required': True,
            },
            'start_date': {
                'required': True,
            },
            'initial_quantity': {
                'required': True,
            },
            'tank': {
                'required': True,
            },
            'expected_cn': {
                'required': True,
            },
            'undigested_percentage': {
                'required': True,
            },

        }


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


class DailyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyActivity
        fields = '__all__'


class DailyActivityCreateSerializer(serializers.ModelSerializer):
    day_number = serializers.IntegerField(read_only=True)
    initial_quantity = serializers.IntegerField(
        read_only=True,
        source='project.initial_quantity',
    )

    def validate(self, attrs):
        activity_date = attrs.get('activity_date')
        project = attrs.get('project')
        date_exists = DailyActivity.objects.filter(activity_date=activity_date, project=project).exists()
        if date_exists:
            raise serializers.ValidationError(
                {
                    'activity_date': _('Activity date already exists for this project.')
                }
            )
        attrs['expected_cn'] = project.expected_cn
        return attrs

    class Meta:
        model = DailyActivity
        fields = '__all__'
        extra_kwargs = {
            'expected_cn': {
                'read_only': True,
            },

            'activity_date': {
                'required': True,
                'allow_null': False,
            },
            'dead_fish': {
                'required': True,
                'allow_null': False,
            },
            'feed_protein_percentage': {
                'required': True,
                'allow_null': False,
            },
            'feed_percentage': {
                'required': True,
                'allow_null': False,
            },
            'single_fish_weight': {
                'required': True,
                'allow_null': False,
            },
            'project': {
                'required': True,
                'allow_null': False,
            },
        }

    def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        res['project'] = ProjectSerializer(instance.project).data
        extra_data = instance.get_extra_data
        res.update(extra_data)
        print(res)

        return res


class DailyActivitySerializerMixin(serializers.Serializer):
    day_number = serializers.IntegerField(read_only=True)
    initial_quantity = serializers.IntegerField(read_only=True)
    project_total_dead = serializers.IntegerField(read_only=True)
    project_total_live = serializers.IntegerField(read_only=True)
    day_total_live = serializers.IntegerField(read_only=True)
    day_total_weight = serializers.SerializerMethodField(read_only=True, method_name='get_day_total_weight')
    activity_todays_feed = serializers.SerializerMethodField(read_only=True, method_name='get_activity_todays_feed')
    activity_feed_n = serializers.SerializerMethodField(read_only=True, method_name='get_activity_feed_n')
    activity_molas_to_add = serializers.SerializerMethodField(read_only=True, method_name='get_activity_molas_to_add')

    def get_day_total_weight(self, instance):
        day_total_live = getattr(instance, 'day_total_live', 0)
        total_weight = day_total_live * instance.single_fish_weight
        return total_weight

    def get_activity_todays_feed(self, instance):
        day_total_live = getattr(instance, 'day_total_live', 0)
        total_weight = day_total_live * instance.single_fish_weight
        return round(total_weight * instance.feed_percentage / 100, 4)

    def get_activity_feed_n(self, instance):
        undigested_percentage = instance.project.undigested_percentage
        value = float(instance.todays_feed) * 0.90 * float(undigested_percentage / 100) * float(
            instance.feed_protein_percentage / 100) * 0.16
        return round(value, 10)

    def get_activity_molas_to_add(self, instance):
        feed_n = calculate_feed_n(instance)
        feed_c = calculate_feed_c(instance)
        value = (float(feed_n * float(instance.expected_cn)) - float(feed_c)) / 0.28
        return round(value, 2)


class DailyActivityListSerializer(DailyActivitySerializerMixin, serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = DailyActivity
        fields = '__all__'
