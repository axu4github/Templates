from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    """ 租户表 """
    name = models.CharField("租户名称", max_length=255)
    code = models.CharField("租户代码", max_length=255)
    type = models.CharField("租户类型", max_length=255)
    details = models.TextField("租户详情", default="")
    created = models.DateTimeField("租户创建时间", auto_now_add=True)
    modified = models.DateTimeField("租户修改时间", auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    modified = models.DateTimeField("修改时间", auto_now=True)
