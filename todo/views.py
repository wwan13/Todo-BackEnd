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

    # permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        auth_token = self.request.headers['Authorization']
        token = Token.objects.get(key = auth_token)
        current_user = token.user
        print(auth_token)
        print(current_user)

        filter_keyword = self.request.query_params.get('filter', None)

        if filter_keyword == 'ongoing':
            queryset = Todo.objects.filter(state = 'ongoing').filter(author = current_user)
        elif filter_keyword == 'complete':
            queryset = Todo.objects.filter(state = 'complete').filter(author = current_user)
        else:
            queryset = Todo.objects.order_by('-state', '-timeline').filter(author = current_user)
        
        return queryset


    def create(self, *args, **kwargs):
        
        new_todo = Todo()

        auth_token = self.request.headers['Authorization']
        token = Token.objects.get(key = auth_token)
        current_user = token.user

        new_todo.author = current_user

        new_todo.contents = self.request.data["contents"]
        new_todo.date = self.request.data["date"]
        new_todo.save()

        serializer = TodoSerializer(new_todo)

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