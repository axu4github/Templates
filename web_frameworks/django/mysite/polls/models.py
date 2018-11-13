import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Tenant(models.Model):
    name = models.CharField("租户名称", max_length=255)
    code = models.CharField("租户代码", max_length=255)
    status = models.CharField("租户状态", max_length=20)
    type = models.CharField("租户类型", max_length=255)
    details = models.TextField("租户详情", default="")
    created = models.DateTimeField("租户创建时间", auto_now=True)
    modified = models.DateTimeField("租户修改时间", auto_now_add=True)
