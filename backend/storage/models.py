from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class MyFile(models.Model):
    res_path = models.CharField(max_length=100, verbose_name="静态资源路径")
    size = models.BigIntegerField(verbose_name="文件大小")
    date_joined = models.DateTimeField(verbose_name="创建时间")
    ban = models.BooleanField(verbose_name='禁用', default=False)

    class Meta:
        verbose_name = verbose_name_plural = '文件'
    
    def __str__(self):
        return self.res_path

class Catalogue(MPTTModel):
    name = models.CharField(max_length=50, verbose_name="文件(夹)名")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_file = models.BooleanField(verbose_name='是否为文件', default=False)
    extension = models.CharField(max_length=12, null=True, blank=True, verbose_name="扩展名")
    my_file = models.ForeignKey(MyFile, on_delete=models.CASCADE, null=True, blank=True, related_name='my_catalogue')

    class Meta:
        verbose_name = verbose_name_plural = '目录'

    def __str__(self):
        return self.name