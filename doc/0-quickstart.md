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

## 직렬화
[tutorial/quickstart/serializers.py](../quickstart/serializers.py) 파일 생성

## 뷰

## URL

## 페이지네이션

## 설정

## API 테스트
