"""circe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from hops import views


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('groups/', views.classgroup_list),
    path('group/<int:pk>', views.classgroup_detail),
    path('attendance/<int:group_id>/<str:date>/', views.attendance, name='attendance_detail'),
    path('create_attendance/<int:group_id>/', views.create_attendance_sheet, name = 'create_attend_sheet'),
    path('studentattendance/<int:studentid>', views.student_attendance, name = 'attendance of the student'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    #path("groups/", views.trainingGroups, name="trainingGroups"),
    #path('api-auth/', include('rest_framework.urls'))
]
