from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import TodoSerializer
from .models import Todo
from todo import serializer

# Create your views here.

class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    # permission_classes= [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        new_todo = Todo()
        new_todo.author = request.user
        new_todo.contents = request.data["contents"]
        new_todo.date = request.data["date"]
        new_todo.save()

        serializer = TodoSerializer(new_todo)

        return Response(serializer.data)