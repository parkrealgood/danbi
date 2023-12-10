from rest_framework.test import APITestCase

from common.tests_data import create_test_data
from task.models import Task, SubTask
from user.models import User, Team


class TestCase(APITestCase):
    def setUp(self):
        create_test_data()
        self.tasks = Task.objects.all()
        self.sub_tasks = SubTask.objects.all()
        self.users = User.objects.all()
        self.teams = Team.objects.all()

    def login(self, user):
        self.client.force_authenticate(user=user)
