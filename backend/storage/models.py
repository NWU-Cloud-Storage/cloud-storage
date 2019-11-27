'''
存储功能app的models
'''
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db.models import F

from mptt.models import MPTTModel, TreeForeignKey


class MyFile(models.Model):
    '''
    文件model类，存储文件所在的静态资源路径，文件大小，创建时间，是否被禁用，引用次数。
    文件和目录之间是一对多关系，因为同一个文件在两个人的目录下，或者在群组目录下是不同的。
    如果已经没有任何一个目录保存着文件，那么文件应该被删除。
    每当有新的外键引用该文件，文件的引用次数要加1，同理外键被删除应该减1，减到0文件就要被删除。
    '''
    res_path = models.CharField(max_length=100, verbose_name="静态资源路径")
    size = models.BigIntegerField(verbose_name="文件大小")
    date_joined = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    reference_count = models.IntegerField(verbose_name="引用次数", default=0)
    is_legal = models.BooleanField(verbose_name='是否合法', default=True)

    class Meta:
        verbose_name = verbose_name_plural = '文件'

    def __str__(self):
        return self.res_path

class Catalogue(MPTTModel):
    '''
    目录model类，个人的目录，群组的目录，分享的目录都会引用这个对象为外键。
    一个人通过分享功能可以把文件（夹）分享给另一个人或者一个群组，
    这时另一个人或群组并保存到自己的仓库里以后，就能够独立管理这个文件（夹）。
    要注意的是，一定要先建立File，再把File的引用当作参数来建立Catalogue。
    不可以建立好Catalogue之后，再把File的引用更新进去。
    '''

    name = models.CharField(
        max_length=50,
        verbose_name="文件(夹)名"
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )
    is_file = models.BooleanField(
        default=False,
        verbose_name='是否为文件'
    )
    extension = models.CharField(
        max_length=12,
        null=True, default=None,
        verbose_name="扩展名"
    )
    my_file = models.ForeignKey(
        MyFile,
        on_delete=models.CASCADE,
        null=True, default=None,
        related_name='my_catalogue'
    )
    is_shared = models.BooleanField(
        default=False,
        verbose_name="是否已经分享"
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="修改日期"
    )

    class Meta:
        verbose_name = verbose_name_plural = '目录'

    def __str__(self):
        return self.name

# dispatch_uid 的作用是防止多次调用，具体原理不清楚。要求是个unique hashable类型的就行，那我就写一些中文了。
@receiver(post_save, sender=Catalogue, dispatch_uid="新建一个目录之后，文件引用数应该加1")
def after_created_catalogue(instance, created, **kwargs):
    if created and instance.is_file:
        my_file = instance.my_file
        my_file.reference_count = F('reference_count') + 1
        my_file.save()

@receiver(pre_delete, sender=Catalogue, dispatch_uid="删除一个目录前，文件引用数应该减1")
def before_delete_catalogue(instance, **kwargs):
    if instance.is_file:
        my_file = instance.my_file
        my_file.reference_count = F('reference_count') - 1
        my_file.save()

@receiver(post_save, sender=MyFile, dispatch_uid="当文件引用数为0，文件自动被删除")
def after_save_file(instance, created, **kwargs):
    if created:
        return
    instance.refresh_from_db()
    if instance.reference_count == 0:
        instance.delete()