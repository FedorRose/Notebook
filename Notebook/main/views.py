from django.shortcuts import render
from rest_framework import mixins, generics
from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import *


class NoteViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Note.objects.all().filter(category=1)
    serializer_class = NoteSerializer
    lookup_field = 'data'


class NoteListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Note.objects.all().filter(category=2)
    serializer_class = NoteSerializer
