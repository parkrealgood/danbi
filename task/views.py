from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from conf.responses import common_response
from task.serializers import TaskRetrieveSerializer, TaskCreateSerializer
from task.services import TaskService
from task.models import Task, SubTask


class TaskViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    create_serializer = TaskCreateSerializer
    retrieve_serializer = TaskRetrieveSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'update':
            return TaskCreateSerializer
        elif self.action == 'retrieve':
            return TaskRetrieveSerializer
        elif self.action in ['complete_task', 'complete_sub_task']:
            return None
        return TaskRetrieveSerializer

    def get_queryset(self):
        queryset = Task.objects.select_related(
            'create_user', 'create_user__team', 'team'
        ).prefetch_related(
            'sub_tasks', 'sub_tasks__team'
        ).filter(
            Q(team=self.request.user.team) |
            Q(sub_tasks__team=self.request.user.team)
        ).distinct().order_by(
            'is_complete', '-created_at'
        )
        return queryset

    @swagger_auto_schema(
        operation_summary='업무 리스트 조회 API',
        manual_parameters=[],
        responses={200: TaskRetrieveSerializer(many=True)},
        tags=['task']
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.retrieve_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    @swagger_auto_schema(
        operation_summary='업무 상세 조회 API',
        manual_parameters=[],
        responses={200: TaskRetrieveSerializer()},
        tags=['task']
    )
    @common_response
    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        data = self.retrieve_serializer(task).data if task else None

        return Response({'data': data})

    @swagger_auto_schema(
        operation_summary='업무 생성 API',
        request_body=TaskCreateSerializer,
        responses={200: TaskRetrieveSerializer()},
        tags=['task']
    )
    @common_response
    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        task = TaskService().create_task(
            self.request.user.id,
            serializer.validated_data.get('title'),
            serializer.validated_data.get('content'),
            serializer.validated_data.get('sub_task_team_ids')
        )
        return Response(status=201, data={'data': self.retrieve_serializer(task).data})

    @swagger_auto_schema(
        operation_summary='업무 수정 API',
        operation_description='* 수정이 필요한 필드만 전달해야 합니다.',
        request_body=TaskCreateSerializer,
        responses={200: TaskRetrieveSerializer()},
        tags=['task']
    )
    @common_response
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        updated_task = TaskService().update_task(
            task.pk,
            self.request.user.id,
            serializer.validated_data.get('title'),
            serializer.validated_data.get('content'),
            serializer.validated_data.get('sub_task_team_ids')
        )

        return Response({'data': self.retrieve_serializer(updated_task).data})

    @swagger_auto_schema(
        operation_summary='상위 업무 완료 API',
        responses={200: TaskRetrieveSerializer()},
        tags=['task']
    )
    @action(detail=True, methods=['post'], url_path='complete', url_name='task-complete')
    @common_response
    def complete_task(self, request, *args, **kwargs):
        task = self.get_object()
        completed_task = TaskService().complete_task(task.id, self.request.user.id)
        return Response({'data': self.retrieve_serializer(completed_task).data})


class SubTaskViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    retrieve_serializer = TaskRetrieveSerializer

    def get_queryset(self):
        queryset = SubTask.objects.select_related(
            'task', 'team'
        ).filter(
            Q(team=self.request.user.team) |
            Q(task__team=self.request.user.team)
        ).distinct()
        return queryset

    @swagger_auto_schema(
        operation_summary='하위 업무 완료 API',
        operation_description='* 하위 업무가 모두 완료되면 상위 업무도 완료됩니다.',
        responses={200: TaskRetrieveSerializer()},
        tags=['task']
    )
    @action(detail=True, methods=['post'], url_path='complete', url_name='complete')
    @common_response
    def complete(self, request, *args, **kwargs):
        sub_task = self.get_object()
        completed_sub_task = TaskService().complete_sub_task(sub_task.id, self.request.user.id)

        return Response({'data': self.retrieve_serializer(completed_sub_task.task).data})
