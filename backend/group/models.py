from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import F

from user.models import User

# Create your models here.

class Group(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='群组名'
    )
    members = models.ManyToManyField(
        User,
        through='MembershipTmp',
        related_name='my_groups'
    )
    intentions = models.ManyToManyField(
        User,
        through='Intention',
        related_name='intent_group'
    )

    num_of_members = models.IntegerField(verbose_name='群人数', default=0)

    class Meta:
        verbose_name = verbose_name_plural = '群组'

    def __str__(self):
        return self.name


class MembershipTmp(models.Model):
    PERMISSIONS = [
        ('master', '创建人'),
        ('manager', '管理员'),
        ('member', '成员'),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=7,
        choices=PERMISSIONS,
        default='member',
        verbose_name='权限'
    )

    class Meta:
        verbose_name = verbose_name_plural = '组员'
        indexes = [
            models.Index(fields=['group', 'user']),
        ]

    def __str__(self):
        return  '【' + self.permission + '】' + self.group.name + '.' + self.user.username

    def __gt__(self, other):
        my_permission = self.permission
        others_permission = other.permission
        if others_permission == 'master' \
            or others_permission == my_permission == 'manager' \
            or my_permission == 'member':
            return False
        return True

class Intention(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_intended = models.DateTimeField(verbose_name='申请时间', auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = '加群申请'
        indexes = [
            models.Index(fields=['group', 'user']),
        ]

    def __str__(self):
        return self.user.username + ' 申请加入 ' + self.group.name

    def consent(self):
        """
        同意申请
        """
        membership, created = MembershipTmp.objects.get_or_create(group=self.group, user=self.user)
        self.delete()
        return membership

    def reject(self):
        """
        拒绝申请
        """
        self.delete()

@receiver(post_save, sender=MembershipTmp, dispatch_uid="加入群以后，群人数加1")
def after_join_a_group(instance, created, **kwargs):
    if created:
        group = instance.group
        group.num_of_members = F('num_of_members') + 1
        group.save()
        group.refresh_from_db()

@receiver(post_delete, sender=MembershipTmp, dispatch_uid="退出群以后，群人数减1")
def after_leave_a_group(instance, **kwargs):
    group = instance.group
    group.num_of_members = F('num_of_members') - 1
    group.save()
    group.refresh_from_db()
