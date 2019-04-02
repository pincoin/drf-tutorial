# 1. 직렬화

## 소개

코드 하일라이트 관리를 위한 예제 프로그램

* 소스 코드: https://github.com/encode/rest-framework-tutorial
* 데모: https://restframework.herokuapp.com/

### 필요한 패키지 설치
`django`, `djangorestframework` 패키지는 이미 설치했음

```
pip install pygments
```

## `snippets` 앱 만들기
`tutorial` 프로젝트는 이미 만들었음

```
python manage.py startapp snippets
```

### 앱 등록
[tutorial/settings.py](../tutorial/settings.py) 파일을 수정해서 `snippets` 앱을 등록한다.

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
    'snippets.apps.SnippetsConfig',
)
```

## 모델 선언
[0. 퀵스타트](0-quickstart.md)에서는 장고 기본 `User`, `Group` 모델을 사용했기 때문에 모델을 선언하지 않았다.

```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)
```

### 마이그레이션

```
python manage.py makemigrations 
python manage.py migrate
```

## 직렬화 클래스 선언

## ModelSerializer 사용하기

## 직렬화 클래스와 장고 뷰 연동

## API 테스트

## 복습
