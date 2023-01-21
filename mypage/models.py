from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class WeightBF(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(default="", max_length=30)
    pub_date = models.DateTimeField(default=timezone.now)

    date = models.DateTimeField(null=False)
    weight = models.FloatField(null=False)
    bf_percent = models.FloatField(null=False)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])


class FatLossJourneyParams(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(default="", max_length=30)
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    initial_cut_date = models.DateTimeField()
    cal_deficit_per_day = models.IntegerField()
    days_journey_length = models.IntegerField()  # journey length in days
    weight_initial_dry = models.FloatField()
    bf_initial = models.FloatField()
    delta_bf_initial = models.FloatField()  #uncertainty
    deficit_days_per_week = models.IntegerField()
    daily_deficit_uncertainty = models.IntegerField(default=200)
    
    def dc_cons_opt(self):
        return [self.daily_deficit_uncertainty, -1 * self.daily_deficit_uncertainty]


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    @classmethod
    def get_most_recent(cls, username):
        """Returns most recently created record."""

        user = User.objects.get(username=username)  # .values()
        try:
            params = cls.objects.get(owner=user)
        except:
            return None
        return params
