from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Sc(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.CharField(max_length=30, verbose_name='客户端')
    score = models.IntegerField(verbose_name='分数', default=0,
                                validators=[MaxValueValidator(10000000), MinValueValidator(1)])

    class Meta:
        verbose_name = '分数记录'
        verbose_name_plural = verbose_name

