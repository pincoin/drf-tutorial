from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Django 사용자 조회 및 수정 가능한 종단 API
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    Django 그룹 조회 및 수정 가능한 종단 API
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
