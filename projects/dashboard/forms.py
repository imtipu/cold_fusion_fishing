from typing import Any

from crispy_forms.layout import Layout, Field
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from projects.models import Project, DailyActivity


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Start Date',
        required=True, widget=forms.DateInput(attrs={
            'type': 'date',
            'value': timezone.now().date(),
        }))

    end_date = forms.DateField(
        label='End Date',
        required=False, widget=forms.DateInput(attrs={
            # 'class': 'input input-sm rounded-sm input-bordered w-full'
            #          ' outline-none focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-transparent',
            'type': 'date',
            'value': '',
        }))
    #
    initial_quantity = forms.IntegerField(
        label='Initial Quantity',
        min_value=1,
        required=True, widget=forms.NumberInput(attrs={
            'type': 'number',
            'min': 1,
            'placeholder': '1000',
            'value': '1'
        }))

    class Meta:
        model = Project
        fields = '__all__'


class ProjectUpdateForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Start Date',
        required=True, widget=forms.DateInput(attrs={
            'type': 'date',
        }))

    end_date = forms.DateField(
        label='End Date',
        required=False, widget=forms.DateInput(attrs={
            'type': 'date',
        }))

    class Meta:
        model = Project
        fields = [
            'title', 'tank', 'start_date', 'end_date', 'initial_quantity', 'expected_cn',
            'undigested_percentage', 'description'
        ]


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
            'placeholder': '100',
            'value': '1'
        }))

    feed_percentage = forms.DecimalField(
        label='Feed (%)',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'max': 100,
            'placeholder': '4',
            'value': '1'
        }))

    singe_fish_weight = forms.DecimalField(
        label=_('Single Fish Weight (gm)'),
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'placeholder': '50',
            'value': '1'
        }))

    feed_protein_percentage = forms.DecimalField(
        label='Feed Protein (%)',
        required=True, widget=forms.NumberInput(attrs={
            'class': 'input input-sm rounded-md input-bordered w-full',
            'type': 'number',
            'min': 0,
            'max': 100,
            'placeholder': '45',
            'value': '1'
        }))

    class Meta:
        model = DailyActivity
        fields = [
            'activity_date',
            'dead_fish',
            'feed_percentage',
            'singe_fish_weight',
            'feed_protein_percentage',
        ]

    def clean_activity_date(self):
        activity_date = self.cleaned_data.get('activity_date')
        if activity_date > timezone.now().date():
            raise forms.ValidationError('Activity date cannot be greater than today.')
        return activity_date

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk is None:
            project = instance.project
            expected_cn = project.expected_cn
            instance.expected_cn = expected_cn
        instance.save()
        return instance
