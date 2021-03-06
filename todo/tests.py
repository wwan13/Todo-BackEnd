from django.http import response
from django.test import TestCase, Client
from .models import Todo
from datetime import datetime
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your tests here.

class TodoTest(TestCase):

    URL = "/api/todo/"
    client = Client()

    def setUp(self):
        """
        테스트 시작 전 데이터 세팅
        """

        user = User.objects.create()

        todo = Todo.objects.create(
            date = datetime.now(),
            contents = "aassdd",
            author = user
        )

    def tearDown(self):
        """
        테스트 종료 후 데이터 삭제
        """

        Todo.objects.all().delete()
        
    
    # 모든 단위테스트는 "test_"로 시작해야함
    def test_get_todo_list_success(self):

        response = self.client.get(self.URL, content_typt = "application/json")

        self.assertEqual(response.status_code, 200)


    def test_make_todo_success(self):

        header = {"Authorization" : "f6b143bda885e4fbd8c90227a879eda162c3dadb",} 

        data = {
            "date" : "2020-10-21",
            "contents" : "unit test",
        }

        response = self.client.post(self.URL, json.dumps(data), content_type="application/json", **header)

        self.assertEqual(response.status_code, 200)
