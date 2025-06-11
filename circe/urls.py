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
from hops import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('group/<int:pk>', views.classgroup_detail),
    path('teacher/<int:teacher_id>/groups/', views.teacher_groups, name='teacher_groups'),
    #path('attendance/<int:group_id>/<str:date>/', views.attendance, name='attendance_detail'),
    path('create_attendance/<int:group_id>/', views.create_attendance_sheet, name = 'create_attend_sheet'),
    path('update_attendance/<int:groupID>/<int:studentID>/<int:attendType>/', views.attendance_update, name = 'update_attendance_record'),
    path('studentattendance/<int:studentid>', views.student_attendance, name = 'attendance of the student'),
    path('presences/', views.presence_types, name = 'presence types'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),

    # API Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
