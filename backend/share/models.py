from django.db import models
from storage.models import Catalogue

# Create your models here.

class Share(models.Model):
    url = models.CharField(max_length=32, verbose_name='分享链接', primary_key=True)
    pwd = models.CharField(max_length=4, verbose_name='提取码', null=True)
    is_unlimited = models.BooleanField(verbose_name='是否永久共享', default=True)
    expiration = models.DateTimeField(verbose_name='过期时间点', null=True, default=None)
    my_catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '分享'
    
    def __str__(self):
        return self.url