from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


# Create your models here.



@python_2_unicode_compatible
class Share(models.Model):
    def __str__(self):
        return self.share_code

    share_code = models.CharField(max_length=200, unique=True)
    share_name = models.CharField(max_length=200, default='')
    share_buy_price = models.FloatField(default=0.0)
    share_buy_amount = models.IntegerField(default=0)
    share_5day_max_agr = models.FloatField(default=0.0)
    share_7day_mwa_agr = models.FloatField(default=0.0)
    share_stop_price = models.FloatField(default=0.0)
    double_avg_crossed = models.BooleanField(default=False)
    supervision_status = models.BooleanField(default=False)
    max_risk = models.FloatField(default=0.0)
