from django.db.models import Q

from conf.tests import TestCase


class TaskTestCase(TestCase):

    def test_업무_리스트_조회(self):
        user = self.users.filter(username='김윙크').first()
        resp = self.client.get('/task/task/', headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']
        for task in resp_data:
            keys = set(task.keys())
            for key in ['id', 'create_user', 'team', 'title', 'content',
                        'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
                self.assertIn(key, keys)
                keys.remove(key)
            self.assertEqual(len(keys), 0)
        self.assertEqual(resp.status_code, 200)

    def test_업무_상세_조회(self):
        user = self.users.filter(username='김윙크').first()
        task_id = self.tasks.filter(
            Q(team=user.team) |
            Q(sub_tasks__team=user.team)).first().id
        resp = self.client.get(f'/task/task/{task_id}/', headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']
        keys = set(resp_data.keys())
        for key in ['id', 'create_user', 'team', 'title', 'content',
                    'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
            self.assertIn(key, keys)
            keys.remove(key)
        self.assertEqual(len(keys), 0)
        self.assertEqual(resp.status_code, 200)

    def test_윙크_업무_생성_하위_업무_없음(self):
        user = self.users.filter(username='김윙크').first()
        data = {
            'title': '업무 업무',
            'content': '윙크 업무 내용'
        }
        resp = self.client.post('/task/task/', data=data, headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']
        keys = set(resp_data.keys())
        for key in ['id', 'create_user', 'team', 'title', 'content',
                    'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
            self.assertIn(key, resp_data)
            keys.remove(key)
        sub_tasks = resp_data['sub_tasks']
        self.assertEqual(len(keys), 0)
        self.assertEqual(sub_tasks, [])
        self.assertEqual(resp.status_code, 201)

    def test_윙크_업무_생성_하위_업무_있음(self):
        user = self.users.filter(username='김윙크').first()
        data = {
            'title': '업무 업무',
            'content': '윙크 업무 내용',
            'sub_task_team_ids': [3, 4]
        }
        resp = self.client.post('/task/task/', data=data, headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']
        keys = set(resp_data.keys())
        for key in ['id', 'create_user', 'team', 'title', 'content',
                    'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
            self.assertIn(key, resp_data)
            keys.remove(key)

        sub_tasks = resp_data['sub_tasks']
        for sub_task in sub_tasks:
            sub_task_keys = set(sub_task.keys())
            for key in ['id', 'team', 'is_complete', 'completed_date', 'created_at', 'updated_at']:
                self.assertIn(key, sub_task_keys)
                sub_task_keys.remove(key)
            self.assertEqual(len(sub_task_keys), 0)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(keys), 0)
        self.assertEqual(len(sub_tasks), 2)

    def test_윙크_업무_수정(self):
        user = self.users.filter(username='김윙크').last()
        data = {
            'title': '수정된 업무 타이틀',
            'content': '수정된 업무 내용',
            'sub_task_team_ids': [2]
        }
        task_id = self.tasks.filter(create_user=user).first().id
        resp = self.client.put(f'/task/task/{task_id}/', data=data, headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']

        keys = set(resp_data.keys())
        sub_task_team_id_list = []
        for key in ['id', 'create_user', 'team', 'title', 'content',
                    'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
            self.assertIn(key, resp_data)
            keys.remove(key)
        for sub_task in resp_data['sub_tasks']:
            sub_task_team_id_list.append(sub_task['team']['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_data['title'], '수정된 업무 타이틀')
        self.assertEqual(resp_data['content'], '수정된 업무 내용')
        self.assertEqual(sub_task_team_id_list, [2])

    def test_하위_업무_완료_성공(self):
        user = self.users.filter(username='김블라').last()
        sub_task_id = self.sub_tasks.filter(team=user.team).first().id
        resp = self.client.post(f'/task/sub-task/{sub_task_id}/complete/', headers={'X-User-Id': user.id})
        resp_data = resp.json()['data']
        keys = set(resp_data.keys())
        is_complete = None
        for key in ['id', 'create_user', 'team', 'title', 'content',
                    'is_complete', 'completed_date', 'created_at', 'updated_at', 'sub_tasks']:
            self.assertIn(key, resp_data)
            keys.remove(key)
            for sub_task in resp_data['sub_tasks']:
                sub_task_keys = set(sub_task.keys())
                for key in ['id', 'team', 'is_complete', 'completed_date', 'created_at', 'updated_at']:
                    self.assertIn(key, sub_task_keys)
                    sub_task_keys.remove(key)
                self.assertEqual(len(sub_task_keys), 0)
                if sub_task['id'] == sub_task_id:
                    is_complete = sub_task['is_complete']

        self.assertEqual(len(keys), 0)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(is_complete, True)
