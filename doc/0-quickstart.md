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

이 예제는 장고 기본 설치 `User`, `Group` 모델이 설치된다. 마이그레이션했을 때 각각의 테이블은 `auth_user`, `auth_group` 테이블이 만들어진다.

## 뷰

[tutorial/quickstart/views.py](../quickstart/views.py) 파일 수정

```python
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
```

`ModelViewSet`을 상속하고 `queryset`, `serializer_class`를 선언한다.

## URL

```python
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from quickstart import views

# 뷰셋과 라우터를 연결하여 자동으로 URL 설정 등록
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # 라우터 기본 URL 설정
    path('', include(router.urls)),

    # 로그인, 로그아웃 뷰 설정 (운영에서는 사용 안 함)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('admin/', admin.site.urls),
]
```
기본 뷰셋과 라우터를 사용하지 않고 API URL을 직접 다루려면 일반적인 클래스형 뷰를 사용하고 URL 설정을 명시적으로 작성해야 한다.

## 페이지네이션

[tutorial/settings.py](../tutorial/settings.py) 파일을 수정하여 다음 내용을 추가한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

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
