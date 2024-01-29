from rest_framework.generics import *
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class FishTankDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = FishTankDetailSerializer
    queryset = FishTank.objects.all()

    def get_queryset(self):
        return FishTank.objects.select_related(
            'current_project'
        ).annotate(
            total_dead=models.Sum(
                'current_project__daily_activities__dead_fish',
                output_field=models.IntegerField(),
                default=0
            ),
            total_live=models.F('current_project__initial_quantity') - models.F('total_dead'),
        ).all()


class FishTankDropDownlistAPIView(ListAPIView):
    serializer_class = FishTankListSerializer
    queryset = FishTank.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for item in queryset:
            data.append({
                'label': item.title,
                'value': item.pk,
            })

        print(data)

        return Response(data)
