from django.contrib import admin
from mypage.models import FatLossJourneyParams, WeightBF

# Register your models here.
@admin.register(FatLossJourneyParams)
class FatLossJourneyParamsAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'pub_date',
        'active',
        'initial_cut_date',
        'cal_deficit_per_day',
        'days_journey_length',
        'weight_initial_dry',
        'bf_initial',
        'delta_bf_initial',
        'deficit_days_per_week',
    ]
    search_fields = ["owner", "owner__username"]
    list_filter = ["active"]
    date_hierarchy = "pub_date"

@admin.register(WeightBF)
class WeightBFAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'pub_date',
        'username',
        'date',
        'weight',
        'bf_percent',
    ]
    search_fields = ["owner", "owner__username"]
    list_filter = ["username"]
    date_hierarchy = "date"