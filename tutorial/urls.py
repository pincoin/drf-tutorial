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

    # 로그인, 로그아웃 뷰 설정
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]
