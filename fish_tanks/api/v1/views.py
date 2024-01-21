from rest_framework.generics import *

from .serializers import *


class FishTankListAPIView(ListAPIView):
    serializer_class = FishTankListSerializer
    queryset = FishTank.objects.all()

    def get_queryset(self):
        return FishTank.objects.select_related(
            'current_project'
        ).annotate(
            total_dead=models.Sum('current_project__daily_activities__dead_fish', output_field=models.IntegerField(),
                                  default=0),
            total_live=models.F('current_project__initial_quantity') - models.F('total_dead'),
        ).all()
