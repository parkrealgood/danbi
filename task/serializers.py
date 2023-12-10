from rest_framework import serializers

from task.models import Task, SubTask
from user.serialzier import UserBaseSerializer, TeamBaseSerializer


class TaskBaseSerializer(serializers.ModelSerializer):
    """ 업무 Base Serializer """
    class Meta:
        model = Task
        fields = ['id', 'create_user_id', 'team_id', 'title', 'content',
                  'is_complete', 'completed_date', 'created_at', 'updated_at']


class SubTaskSerializer(serializers.ModelSerializer):
    """ 하위 업무 Serializer """
    team = TeamBaseSerializer()

    class Meta:
        model = SubTask
        fields = ['id', 'team',
                  'is_complete', 'completed_date', 'created_at', 'updated_at']


class TaskRetrieveSerializer(TaskBaseSerializer):
    """ 업무 조회 시 Serializer"""
    create_user = UserBaseSerializer()
    team = TeamBaseSerializer()
    sub_tasks = SubTaskSerializer(many=True)

    class Meta:
        model = TaskBaseSerializer.Meta.model
        fields = ['id', 'create_user', 'team',
                  'title', 'content',
                  'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']


class TaskCreateSerializer(serializers.Serializer):
    """ 업무 생성 시 Serializer"""
    title = serializers.CharField(max_length=256, help_text='업무 제목')
    content = serializers.CharField(max_length=256, help_text='업무 내용')
    sub_task_team_ids = serializers.ListField(
        child=serializers.IntegerField(help_text='업무를 수행할 팀 ID'), required=False, help_text='업무를 수행할 팀 ID 리스트'
    )
