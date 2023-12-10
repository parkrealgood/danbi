from django.db import transaction
from django.utils.timezone import localtime

from conf.exceptions import CustomApiException
from task.models import Task, SubTask
from user.models import User, Team


class TaskService:

    def _valid_user(self, user_id: int):
        """ 유저 유효성 체크 """
        if not User.objects.filter(id=user_id).exists():
            raise ValueError('존재하지 않는 유저 ID입니다.')

    def _valid_team(self, team_id: int):
        """ 팀 유효성 체크"""
        if not Team.objects.filter(id=team_id).exists():
            raise ValueError('존재하지 않는 팀 ID입니다.')

    def _valid_task(self, task_id: int):
        """ 업무 유효성 체크 """
        if not Task.objects.filter(id=task_id).exists():
            raise ValueError('존재하지 않는 업무 ID입니다.')

    def _valid_sub_task(self, sub_task_id: int):
        """ 하위 업무 유효성 체크 """
        if not SubTask.objects.filter(id=sub_task_id).exists():
            raise ValueError('존재하지 않는 하위 업무 ID입니다.')

    def _valid_task_team_user(self, user_id: int, task_id: int):
        """ 하위 업무 처리 자격 체크"""
        task = self._get_task(task_id)
        user = self._get_user(user_id)
        if task.team.id != user.team.id:
            raise ValueError('해당 업무를 수행할 수 없습니다.')

    def _valid_sub_task_team_user(self, user_id: int, sub_task_id: int):
        """ 하위 업무 처리 자격 체크"""
        sub_task = self._get_sub_task(sub_task_id)
        user = self._get_user(user_id)
        if sub_task.team.id != user.team.id:
            raise ValueError('해당 하위 업무를 수행할 수 없습니다.')

    def _is_create_user(self, create_user_id: int, task_id: int) -> bool:
        """ 작성자 여부 확인 """
        task = self._get_task(task_id)
        if task.create_user.id == create_user_id:
            return True
        return False

    def _is_all_sub_task_complete(self, task_id: int) -> bool:
        """ 하위 업무가 모두 완료 처리되었는지 체크 """
        not_complete_sub_tasks = SubTask.objects.filter(task_id=task_id, is_complete=False)
        if not_complete_sub_tasks.exists():
            return False
        else:
            return True

    def _get_user(self, user_id: int) -> User:
        """ 유저의 팀 조회 """
        return User.objects.filter(id=user_id).first()

    def _get_task(self, task_id: int) -> Task:
        """ 업무 조회 """
        return Task.objects.filter(id=task_id).first()

    def _get_sub_task(self, sub_task_id: int) -> SubTask:
        """ 하위 업무 조회 """
        return SubTask.objects.filter(id=sub_task_id).first()

    def create_task(self, create_user_id: int, title: str,
                    content: str, sub_task_team_ids: list[int]) -> Task:
        """ 업무 생성 """
        self._valid_user(create_user_id)
        create_user = self._get_user(create_user_id)
        self._valid_team(create_user.team.id)
        if sub_task_team_ids:
            for sub_task_team_id in sub_task_team_ids:
                self._valid_team(sub_task_team_id)

        with transaction.atomic():
            task = Task.objects.create(
                create_user=create_user,
                team=create_user.team,
                title=title,
                content=content,
            )

            if sub_task_team_ids:
                for sub_task_team_id in sub_task_team_ids:
                    SubTask.objects.create(task=task, team_id=sub_task_team_id)

        return task

    def update_task(self, task_id: int, create_user_id: int, title: str,
                    content: str, sub_task_team_ids: list[int]) -> Task:
        """ 업무 수정 """
        self._valid_user(create_user_id)
        self._is_create_user(create_user_id, task_id)
        self._valid_task(task_id)

        for sub_task_team_id in sub_task_team_ids:
            self._valid_team(sub_task_team_id)

        task = self._get_task(task_id)

        with transaction.atomic():

            task.title = title
            task.content = content
            task.save()

            sub_tasks = SubTask.objects.filter(task_id=task_id, is_complete=False)
            if sub_tasks:
                exclude_team_list = list(sub_tasks.values_list('team_id', flat=True).distinct())
                sub_tasks.delete()

            if sub_task_team_ids:
                for sub_task_team_id in sub_task_team_ids:
                    if sub_task_team_id not in exclude_team_list:
                        SubTask.objects.create(task=task, team_id=sub_task_team_id)

            return task

    def complete_sub_task(self, sub_task_id: int, user_id: int) -> SubTask:
        """ 하위 업무 완료 처리"""

        self._valid_user(user_id)
        self._valid_sub_task(sub_task_id)
        self._valid_sub_task_team_user(user_id, sub_task_id)

        with transaction.atomic():
            sub_task = self._get_sub_task(sub_task_id)
            if sub_task.is_complete:
                raise CustomApiException('이미 완료된 하위 업무입니다.')
            sub_task.is_complete = True
            sub_task.completed_date = localtime()
            sub_task.save()

            # 하위 Task가 모두 완료되었을 경우, 상위 Task 완료 처리
            if not self._is_all_sub_task_complete(sub_task.task.id):
                self._complete_task(sub_task.task.id)
        return sub_task

    def _complete_task(self, task_id: int) -> Task:
        """ 업무 완료 처리"""
        task = self._get_task(task_id)
        task.is_complete = True
        task.completed_date = localtime()
        task.save()
        return task

    def complete_task(self, task_id: int, user_id: int) -> Task:
        """ 업무 완료 처리"""
        self._valid_task(task_id)
        self._valid_task_team_user(user_id, task_id)

        if not self._is_all_sub_task_complete(task_id):
            raise CustomApiException('하위 업무가 모두 완료되지 않았습니다.')
        task = self._complete_task(task_id)
        return task
