from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializer import TodoSerializer
from .models import Todo

# Create your views here.

class TodoViewSet(ModelViewSet):
    # queryset = Todo.objects.all()
    queryset = Todo.objects.order_by('-state', '-timeline')
    serializer_class = TodoSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):

        print(self.request.query_params.get('filter', ''))

        filter_keyword = self.request.query_params.get('filter', None)

        if filter_keyword == 'ongoing':
            queryset = Todo.objects.filter(state = 'ongoing')
        elif filter_keyword == 'complete':
            queryset = Todo.objects.filter(state = 'ongoing')
        else:
            queryset = Todo.objects.filter(state = 'ongoing')
        
        return queryset


    def create(self, request, *args, **kwargs):
        
        new_todo = Todo()
        # current_user = User.objects.get(username = request.user.name)
        # new_todo.author = current_user
        print(request.user.__dict__)
        new_todo.author = User.objects.get(pk = 1)

        new_todo.contents = request.data["contents"]
        new_todo.date = request.data["date"]
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