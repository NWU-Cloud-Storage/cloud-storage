from django.db import models
from django.contrib.auth.models import User as AuthUser



# Create your models here.

class User(AuthUser):
    nickname = models.CharField(max_length=30, verbose_name='昵称')
    max_size = models.BigIntegerField(verbose_name='最大容量', default=5*2**30)
    used_size = models.BigIntegerField(verbose_name='已用容量', default=0)
    date_last_opt = models.DateTimeField(verbose_name='上次操作时间', auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    def create_a_group(self):
        from group.models import Group, Membership
        my_group = Group.objects.create(name=self.nickname+"的小组")
        Membership.objects.create(group=my_group, user=self, permission='master')
        return my_group
