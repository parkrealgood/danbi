from django.core.management.base import BaseCommand

from common.tests_data import create_test_data


class Command(BaseCommand):
    help = "테스트 데이터 생성"

    def handle(self, *args, **kwargs):
        create_test_data()
        print('생성 완료')
