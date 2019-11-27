from django.db import models
from user.models import User
from storage.models import Catalogue

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=30, verbose_name='群组名')
    members = models.ManyToManyField(
        User,
        through='Membership',
        related_name='my_group'
    )
    intentions = models.ManyToManyField(
        User,
        through='Intention',
        related_name='intent_group'
    )
    storage = models.OneToOneField(
        Catalogue,
        on_delete=models.PROTECT,
        related_name='my_group'
    )

    class Meta:
        verbose_name = verbose_name_plural = '群组'

    def __str__(self):
        return self.name

class Membership(models.Model):
    PERMISSIONS = [
        ('master', '创建人'),
        ('manager', '管理员'),
        ('member', '成员'),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=7, choices=PERMISSIONS, verbose_name='权限')

    class Meta:
        verbose_name = verbose_name_plural = '组员'

    def __str__(self):
        return  '【' + self.permission + '】' + self.group.name + '.' + self.user.username

class Intention(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_intended = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '加群申请'

    def __str__(self):
        return self.user + ' 申请加入 ' + self.group
