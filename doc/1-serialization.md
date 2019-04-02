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
모델이 있으면 이를 JSON 데이터 표현을 위한 직렬화 클래스를 선언해야 한다.

직렬화 클래스는 장고의 폼 클래스의 선언과 매우 흡사하다.

[quickstart/serializers.py](../quickstart/serializers.py) 파일에서는 `UserSerializer`, `GroupSerializer` 클래스를 선언했다.

`UserSerializer`와 `GroupSerializer` 직렬화 클래스는 `HyperlinkedModelSerializer` 클래스를 상속했지만 이번에는 `Serializer` 범용 직렬화 클래스를 상속한다.

```python
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        폼 검증을 마친 데이터로 채운 `Snippet` 새 인스턴스를 만들어 반환
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        폼 검증을 마친 데이터로 채운 `Snippet` 기존 인스턴스를 수정해서 반환
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```

## 직렬화 클래스 사용해보기

```
python manage.py shell
```

파이참을 이용한다면 Python Console 창에서 바로 명령할 수도 있다.

### Snippet 인스턴스 2개 추가

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()
```

### 파이썬 데이터 타입으로 확인
```python
serializer = SnippetSerializer(snippet)
serializer.data
```

`snippet` 변수는 마지막에 저장한 `hello world` 출력 코드 문자열을 갖고 있다.

출력 결과는 파이썬 데이터 타입으로 출력한다.

```
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

### JSON 타입으로 확인
파이썬 데이터 타입을 JSON 데이터 타입으로 직렬화한다.

```
content = JSONRenderer().render(serializer.data)
content
```

출력 결과는 JSON 데이터 형식으로 출력한다.

```
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```

즉, 직렬화는 파이썬 데이터 타입을 JSON 데이터 타입으로 변환하는 것이다.

### 역직렬화(deserialization)
```python
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```

`content` JSON 데이터 타입을 데이터 형식으로 변환한다.

아래와 같이 해당 데이터를 검증할 수 있다.

```python
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```

### 모델 인스턴스가 아니라 쿼리셋을 직렬화하기
```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
```

## ModelSerializer 사용하기

## 직렬화 클래스와 장고 뷰 연동

## API 테스트

## 복습
