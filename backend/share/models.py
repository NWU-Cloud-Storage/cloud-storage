"""
Share models
"""
import math
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from storage.models import Identifier
from user.models import User
from my_utils.utils import gen_url, after_n_days


class ShareManager(models.Manager):
    """
    Share管理器
    """

    def create_by_user(self, user, cata, days=None, pwd=None):
        """
        由一位user生成的分享链接（不检查）
        """
        length = int(math.log(self.count() + 100000001, 10))
        url = gen_url(length)
        print(pwd)
        while True:
            try:
                self.get(url=url)
                length = length + 1
                url = gen_url(length)
            except ObjectDoesNotExist:
                break
        kwargs = dict()
        kwargs['user'] = user
        kwargs['catalogue'] = cata
        kwargs['url'] = url
        if days is not None:
            kwargs['expiration'] = after_n_days(days)
            kwargs['is_unlimited'] = False
        if pwd:
            kwargs['password'] = pwd
        return self.create(**kwargs)


class Share(models.Model):
    """
    Share model
    """
    url = models.CharField(max_length=32, verbose_name='分享链接', primary_key=True)
    password = models.CharField(max_length=4, verbose_name='提取码', null=True, default=None)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_unlimited = models.BooleanField(verbose_name='是否永久共享', default=True)
    expiration = models.DateTimeField(verbose_name='过期时间点', null=True, default=None)
    catalogue = models.ForeignKey(Identifier, on_delete=models.CASCADE)

    objects = ShareManager()

    class Meta:
        verbose_name = verbose_name_plural = '分享'

    def __str__(self):
        return self.url
