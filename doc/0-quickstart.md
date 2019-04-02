# 퀵스타트

## 환경 설정
### pyenv 환경 설정
```
pyenv virtualenv -p python3.6 3.6.3 drf-tutorial
pyenv shell drf-tutorial
```

### 필요한 패키지 설치
```
pip install django
pip install djangorestframework
```

## 프로젝트 설정
### `tutorial` 프로젝트와 `quickstart` 앱 만들기
```
django-admin startproject tutorial .
python manage.py startapp quickstart
```

### 데이터베이스 마이그레이션
```
python manage.py migrate
```

### 관리자 생성
`admin@exmaple.com` 이메일 주소로 `admin` 사용자를 만든다. 비밀번호를 두 번 입력한다.

```
python manage.py createsuperuser --email admin@example.com --username admin
```

## DRF 앱 등록 설정

[tutorial/settings.py](../tutorial/settings.py) 파일을 수정하여 `INSTALLED_APPS` 튜플 변수에 `rest_framework` 앱을 등록한다.

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
)
```

## 직렬화
[tutorial/quickstart/serializers.py](../quickstart/serializers.py) **모듈** 파일 생성

```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
```

직렬화 클래스는 JSON 포맷 데이터 표현(data representation)을 선언한다.

`HyperlinkedModelSerializer` 직렬화 클래스를 상속하여 하이퍼링크 관계를 사용한다.

PK와 다른 여러 가지 관계를 사용할 수도 있다.

## 뷰

[tutorial/quickstart/views.py](../quickstart/views.py) 파일 수정

```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```

`ModelViewSet`을 상속하고 `queryset`, `serializer_class`를 선언한다.

## URL

## 페이지네이션


## API 테스트

### 장고 실행

```
python manage.py runserver
```

### CURL 테스트
```bash
curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
```

### 웹 화면 테스트

http://127.0.0.1:8000/users/ 접속
