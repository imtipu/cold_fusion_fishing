from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from projects.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
