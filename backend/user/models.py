from django.db import models
from django.contrib.auth.models import User as AuthUser
from storage.models import Catalogue

# Create your models here.

class User(AuthUser):
    nickname = models.CharField(max_length=30, verbose_name='昵称')
    max_size = models.BigIntegerField(verbose_name='最大容量', default=5*2**30)
    used_size = models.BigIntegerField(verbose_name='已用容量', default=0)
    token = models.CharField(max_length=64, verbose_name='user token', null=True)
    date_last_opt = models.DateTimeField(verbose_name='上次操作时间', auto_now=True)
    storage = models.OneToOneField(
        Catalogue,
        on_delete=models.PROTECT,
        related_name='my_master'
    )

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return self.username
