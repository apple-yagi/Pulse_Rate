from django.db import models
from accounts.models import CustomUser

class Pulse_Rate(models.Model):

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    data = models.FileField(verbose_name='データ')
    fc_low = models.FloatField(verbose_name='上限周波数', default=10)
    fc_high = models.FloatField(verbose_name='下限周波数', default=0)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Pulse_Rate'

        def __str__(self):
            return self.title