from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Tenant(models.Model):
    """ 租户表 """
    name = models.CharField(
        "名称",
        max_length=255,
        blank=True,
        null=True,
        default="")
    code = models.CharField(
        "代码",
        max_length=255,
        blank=True,
        null=True,
        default="")
    status = models.IntegerField(
        "状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    type = models.CharField(
        "类型",
        blank=True,
        null=True,
        max_length=255,
        default="")
    details = models.TextField(
        "详情",
        blank=True,
        null=True,
        default="")
    created = models.DateTimeField(
        "创建时间",
        auto_now_add=True)
    modified = models.DateTimeField(
        "修改时间",
        auto_now=True)


class Profile(models.Model):
    """ 用户表 """
    created = models.DateTimeField(
        "创建时间",
        auto_now_add=True)
    modified = models.DateTimeField(
        "修改时间",
        auto_now=True)
    user = models.OneToOneField(  # 用户
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    tenant = models.ForeignKey(  # 租户
        Tenant,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
