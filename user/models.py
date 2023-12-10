from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from common.models import TimeStampModel


class Team(TimeStampModel):
    name = models.CharField(max_length=150, verbose_name='팀 이름')

    class Meta:
        verbose_name = '팀'

    def __str__(self):
        return self.name

    objects = models.Manager()


class User(AbstractUser, TimeStampModel):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, verbose_name='팀', null=True, blank=True)

    class Meta:
        verbose_name = '유저'
