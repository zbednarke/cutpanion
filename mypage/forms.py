from django import forms
from .models import FatLossJourneyParams, WeightBF


class WeightBFForm(forms.ModelForm):

    date = forms.DateTimeField(label="Date or record", 
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(label='Weight (lbs).  Must not be empty',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bf_percent = forms.FloatField(label='Bf percent (like .12 for 12 percent). Must not be empty', 
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = WeightBF
        fields = [
            'date',
            'weight',
            'bf_percent',
         ]

class FatLossJourneyParamsAddForm(forms.ModelForm):

    initial_cut_date = forms.DateTimeField(label="Date of Cut Start", 
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    cal_deficit_per_day = forms.IntegerField(label='Daily Caloric Deficit',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    days_journey_length = forms.IntegerField(label='Days of the Cut',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight_initial_dry = forms.FloatField(label='Initial Dry Weight (lbs)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bf_initial = forms.FloatField(label='Bodyfat Initial (like .12 for 12 percent)', 
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    delta_bf_initial = forms.FloatField(label='Uncertainty in Bodyfat initial (like .02 for 2 percent)', 
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    deficit_days_per_week = forms.FloatField(label='Deficit Days per Week', 
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = FatLossJourneyParams
        fields = [
            'initial_cut_date',
            'cal_deficit_per_day',
            'days_journey_length',
            'weight_initial_dry',
            'bf_initial',
            'delta_bf_initial',
            'deficit_days_per_week',
         ]
        # widgets = {
        #     'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        # }