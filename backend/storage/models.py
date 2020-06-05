"""
存储功能app的models
"""
from django.db import models
from django.db.models import F, Q
from django.db.models import Count
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

from group.models import Group
from user.models import User


class File(models.Model):
    """
    文件model类，存储文件所在的静态资源路径，文件大小，创建时间，是否被禁用，引用次数。
    文件和目录之间是一对多关系，因为同一个文件在两个人的目录下，或者在群组目录下是不同的。
    如果已经没有任何一个目录保存着文件，那么文件应该被删除。
    每当有新的外键引用该文件，文件的引用次数要加1，同理外键被删除应该减1，减到0文件就要被删除。
    """
    file = models.FileField(upload_to='upload/')
    size = models.BigIntegerField(verbose_name="文件大小")
    date_joined = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    reference_count = models.IntegerField(verbose_name="引用次数", default=0)
    is_legal = models.BooleanField(verbose_name='是否合法', default=True)

    class Meta:
        verbose_name = verbose_name_plural = '文件'

    def __str__(self):
        return self.file.name


# class CatalogueManager(models.Manager):
#     """
#     目录管理器
#     """
#     def create_root_by_user(self, user):
#         """为用户创建一个根目录（仓库）"""
#         return self.create(
#             name='user '+str(user.username)+' root',
#             user=user
#         )
#     def create_root_by_group(self, group):
#         """为群组创建一个根目录（仓库）"""
#         return self.create(
#             name='group '+str(group.id)+' root',
#             group=group
#         )
#     def create_by_parent(self, name, parent, my_file=None, extension=None):
#         """创建一个子文件夹"""
#         if my_file:
#             return self.create(
#                 name=name, parent=parent,
#                 is_file=True, my_file=my_file, extension=extension
#             )
#         return self.create(name=name, parent=parent)


class Identifier(MPTTModel):
    """
    目录model类，个人的目录，群组的目录，分享的目录都会引用这个对象为外键。
    一个人通过分享功能可以把文件（夹）分享给另一个人或者一个群组，
    这时另一个人或群组并保存到自己的仓库里以后，就能够独立管理这个文件（夹）。
    要注意的是，一定要先建立File，再把File的引用当作参数来建立Catalogue。
    不可以建立好Catalogue之后，再把File的引用更新进去。
    """

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
        null=True, blank=True, default=None,
        verbose_name="扩展名"
    )
    my_file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        null=True, blank=True, default=None,
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '目录'
        constraints = [
            models.CheckConstraint(
                check=(
                              Q(is_file__exact=True)
                              & Q(my_file__isnull=False)
                              & Q(extension__isnull=False)
                      ) | (
                              Q(is_file__exact=False)
                              & Q(my_file__isnull=True)
                              & Q(extension__isnull=True)
                      ),
                name='file_or_directory'
            )
        ]

    # objects = CatalogueManager()

    def __str__(self):
        return self.name

    def copy_to(self, target):
        """
        递归拷贝。
        调用之前一定要做检查，防止死循环。
        可以使用check_des_not_src_children
        """
        new_cata = Identifier(
            name=self.name,
            is_file=self.is_file,
            my_file=self.my_file,
            extension=self.extension,
            owner=self.owner
        )
        new_cata.insert_at(target, 'first-child', save=True)
        children = self.get_children()
        for child in children:
            child.copy_to(new_cata)


class Storage(models.Model):
    """
    存储库类。
    """
    root_identifier = models.ForeignKey(Identifier, on_delete=models.CASCADE, null=True, default=None)
    created_time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, through='Membership')
    is_personal_storage = models.BooleanField(verbose_name="是否为个人存储库", default=False)
    invite_link = models.URLField(verbose_name='邀请链接')

    class Meta:
        ...
        # constraints = [
        #     models.CheckConstraint(check=(Q(is_personal_storage=True) & Q()),
        #                            name='personal_or_group')
        # ]
        # TODO 约束：个人存储库只允许一个用户

    def __str__(self):
        return self.root_identifier.name


class Membership(models.Model):
    """
    存储库与用户的关系类
    """
    PERMISSIONS = [
        ('read', '读'),
        ('read_write', '读写'),
        ('owner', '存储库的所有者权限，可以添加、删除成员，修改他人的权限')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    joined_time = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(max_length=10, choices=PERMISSIONS)


# dispatch_uid 的作用是防止多次调用，具体原理不清楚。要求是个unique hashable类型的就行，那我就写一些中文了。
@receiver(post_save, sender=Identifier, dispatch_uid="新建一个目录之后，文件引用数应该加1")
def after_created_catalogue(instance, created, **kwargs):
    if created and instance.is_file:
        my_file = instance.my_file
        my_file.reference_count = F('reference_count') + 1
        my_file.save()


@receiver(pre_delete, sender=Identifier, dispatch_uid="删除一个目录前，文件引用数应该减1")
def before_delete_catalogue(instance, **kwargs):
    if instance.is_file:
        my_file = instance.my_file
        my_file.reference_count = F('reference_count') - 1
        my_file.save()
        instance.refresh_from_db()


@receiver(post_save, sender=File, dispatch_uid="当文件引用数为0，文件自动被删除")
def after_save_file(instance, **kwargs):
    instance.refresh_from_db()
    if instance.reference_count == 0:
        instance.delete()


@receiver(post_save, sender=User, dispatch_uid="用户被创建后，自动为其创建仓库")
def after_create_user(instance, created, **kwargs):
    if not created:
        return
    from .utils import create_storage
    create_storage(instance, is_personal_storage=True)

#
#
# @receiver(post_save, sender=Group, dispatch_uid="群组被创建后，自动为其创建仓库")
# def after_create_group(instance, created, **kwargs):
#     if not created:
#         return
#     Identifier.objects.create(
#         name='group '+str(instance.id)+' root',
#         group=instance
#     )
