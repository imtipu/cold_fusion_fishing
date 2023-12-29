from django import forms

from fish_tanks.models import FishTank


class FishTankForm(forms.ModelForm):
    class Meta:
        model = FishTank
        fields = '__all__'
