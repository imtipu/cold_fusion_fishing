from typing import Any
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from projects.models import Project, DailyActivity


class DailyActivityForm(forms.ModelForm):
    activity_date = forms.DateField(
        label='Date',
        required=True, widget=forms.DateInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'date',
            'value': timezone.now().date(),
        }))

    dead_fish = forms.IntegerField(
        label='Dead',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'placeholder': '100'
        }))

    feed_percentage = forms.DecimalField(
        label='Feed (%)',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'max': 100,
            'placeholder': '4'
        }))

    singe_fish_weight = forms.DecimalField(
        label=_('Single Fish Weight (gm)'),
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'placeholder': '50'
        }))

    undigested_percentage = forms.DecimalField(
        label='Undigested (%)',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'max': 100,
            'placeholder': '10'
        }))

    feed_protein_percentage = forms.DecimalField(
        label='Feed Protein (%)',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'max': 100,
            'placeholder': '45'
        }))

    expected_cn = forms.DecimalField(
        label='Expected C.N.',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'placeholder': '18'
        }))

    class Meta:
        model = DailyActivity
        fields = [
            'activity_date',
            'dead_fish',
            'feed_percentage',
            'singe_fish_weight',
            'undigested_percentage',
            'feed_protein_percentage',
        ]

    def clean_activity_date(self):
        activity_date = self.cleaned_data.get('activity_date')
        if activity_date > timezone.now().date():
            raise forms.ValidationError('Activity date cannot be greater than today.')
        return activity_date

