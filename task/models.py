from django.db import models

from common.models import TimeStampModel


class Task(TimeStampModel):
    create_user = models.ForeignKey(
        'user.User', on_delete=models.PROTECT, verbose_name='생성자', related_name='tasks'
    )
    team = models.ForeignKey(
        'user.Team', on_delete=models.PROTECT, verbose_name='팀', related_name='tasks'
    )
    title = models.CharField(max_length=256, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_complete = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='완료 일자')

    class Meta:
        verbose_name = '업무'

    def __str__(self):
        return f'{self.pk}] {self.title}'

    objects = models.Manager()


class SubTask(TimeStampModel):
    task = models.ForeignKey(
        Task, on_delete=models.PROTECT, verbose_name='상위 업무', related_name='sub_tasks'
    )
    team = models.ForeignKey(
        'user.Team', on_delete=models.PROTECT, verbose_name='팀', related_name='sub_tasks'
    )
    is_complete = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='완료 일자')

    class Meta:
        verbose_name = '하위 업무'

    def __str__(self):
        return f'{self.pk}] {self.task}'

    objects = models.Manager()