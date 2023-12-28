from rest_framework.generics import *

from .serializers import *


class FishTankListAPIView(ListAPIView):
    serializer_class = FishTankSerializer
    queryset = FishTank.objects.all()
