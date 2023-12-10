from task.models import Task, SubTask
from user.models import Team, User


def create_test_data():
    """ 테스트용 데이터 생성"""
    test_data_names = [
        {
            'team_name': '단비',
            'members_names': [
                '김윙크', '김단비'
            ]
        },
        {
            'team_name': '다래',
            'members_names': [
                '김다래'
            ]
        },
        {
            'team_name': '블라블라',
            'members_names': [
                '김블라'
            ]
        },
        {
            'team_name': '철로',
            'members_names': [
                '김철로'
            ]
        },
        {
            'team_name': '땅이',
            'members_names': [
                '김땅이'
            ]
        },
        {
            'team_name': '해태',
            'members_names': [
                '김해태'
            ]
        },
        {
            'team_name': '수피',
            'members_names': [
                '김수피'
            ]
        },
    ]

    for test_data_name in test_data_names:
        team, _ = Team.objects.get_or_create(name=test_data_name['team_name'])
        for member_name in test_data_name['members_names']:
            user, _ = User.objects.get_or_create(username=member_name, password='test_password12!@', team=team)

    user_1 = User.objects.filter(username='김윙크').first()
    user_2 = User.objects.filter(username='김다래').last()
    user_3 = User.objects.filter(username='김블라').last()
    user_4 = User.objects.filter(username='김철로').last()
    user_5 = User.objects.filter(username='김해태').last()

    task1, _ = Task.objects.get_or_create(create_user=user_1, team=user_1.team, title='1번 업무', content='1번 업무 내용')
    task2, _ = Task.objects.get_or_create(create_user=user_1, team=user_1.team, title='2번 업무', content='2번 업무 내용')
    task3, _ = Task.objects.get_or_create(create_user=user_2, team=user_2.team, title='3번 업무', content='3번 업무 내용')

    task1_sub_task1 = SubTask.objects.get_or_create(task=task1, team_id=3)
    task1_sub_task2 = SubTask.objects.get_or_create(task=task1, team_id=4)
    task1_sub_task3 = SubTask.objects.get_or_create(task=task1, team_id=5)
    task2_sub_task1 = SubTask.objects.get_or_create(task=task2, team_id=1)

    return True
