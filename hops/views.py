from datetime import datetime
from django.http import HttpResponse

from .models import Students, ClassGroups, AttendanceSheet, Presence, AttendanceRecord

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, viewsets, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from hops.serializers import GroupSerializer, UserSerializer, GroupsSerializer, AttendanceSerializer,StudentAttendance


@api_view(['GET'])
def classgroup_list(request):
    try:
        if request.method == 'GET':
            queryset = ClassGroups.objects.order_by('id')
            serializer = GroupsSerializer(queryset, many=True)
            return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def classgroup_detail(request, pk):
    group = ClassGroups.objects.get(pk  = pk)
    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['GET','POST'])
@csrf_exempt
def attendance( request, group_id, date=None):
    if request.method == 'GET':
        # Retrieve attendance record by group and date
        attendance_sheet = get_object_or_404(AttendanceSheet, group_id = group_id, date = date)

        # Serialize attendance data
        serializer = AttendanceSerializer(attendance_sheet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def student_attendance( request, studentid):
    student_sheet = AttendanceRecord.objects.filter(studentID = studentid)

    # Serialize attendance data
    serializer = StudentAttendance(student_sheet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)