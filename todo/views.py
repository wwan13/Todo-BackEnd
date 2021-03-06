from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializer import TodoSerializer
from .models import Todo

class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):

        # 유저 헤더가 없을 경우 전체 쿼리셋 리턴
        if 'Authorization' not in self.request.headers:
            return Todo.objects.all()

        current_user = self.get_current_user()

        filter_keyword = self.request.query_params.get('filter', None)

        if filter_keyword == 'ongoing':
            queryset = Todo.objects.filter(state = 'ongoing').filter(author = current_user)
        elif filter_keyword == 'complete':
            queryset = Todo.objects.filter(state = 'complete').filter(author = current_user)
        else:
            queryset = Todo.objects.order_by('-state', '-timeline').filter(author = current_user)
        
        return queryset


    def create(self, *args, **kwargs):

        current_user = self.get_current_user()

        todo = Todo(
            author = current_user,
            contents = self.request.data["contents"],
            date = self.request.data["date"]
        )
        todo.save()

        serializer = TodoSerializer(todo)

        return Response(serializer.data)


    @action(detail = True)
    def set_complete(self, request, *args, **kwargs):

        todo_object = self.get_object()
        todo_object.state = 'complete'
        todo_object.save()

        serializer = TodoSerializer(todo_object)

        return Response(serializer.data)

    @action(detail = True)
    def set_ongoing(self, request, *args, **kwargs):

        todo_object = self.get_object()
        todo_object.state = 'ongoing'
        todo_object.save()

        serializer = TodoSerializer(todo_object)

        return Response(serializer.data)

    def get_current_user(self):

        auth_token = self.request.headers['Authorization']
        token = Token.objects.get(key = auth_token)
        current_user = token.user

        return current_user