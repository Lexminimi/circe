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
from hops.serializers import GroupsSerializer, UserSerializer, GroupDetailSerializer, AttendanceSerializer,StudentAttendance

from .serializers import PresenceSerializer


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
        serializer = GroupDetailSerializer(group)
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

@api_view(['POST'])
def create_attendance_sheet(request, group_id):
    if request.method == 'POST':
        # Use today's date dynamically
        current_date = datetime.now().date().strftime('%Y-%m-%d')
        if AttendanceSheet.objects.filter(date = current_date, group_id = group_id).exists():
            # Retrieve attendance record by group and date
            attendance_sheet = get_object_or_404(AttendanceSheet, group_id=group_id, date = current_date )

            # Serialize attendance data
            serializer = AttendanceSerializer(attendance_sheet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create the attendance sheet with the current date
            new_sheet = AttendanceSheet.objects.create(date = current_date, group_id = group_id)

            # Fetch students and the default presence type
            students = ClassGroups.objects.filter(pk=group_id).values_list('members', flat=True)
            presence_type = Presence.objects.first()

            # Bulk create attendance records
            attendance_records = [
                AttendanceRecord(sheetID=new_sheet, studentID_id=student, presenceID=presence_type)
                for student in students
            ]
            AttendanceRecord.objects.bulk_create(attendance_records)

            # Serialize and return the response
            serializer = AttendanceSerializer(new_sheet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def student_attendance( request, studentid):
    student_sheet = AttendanceRecord.objects.filter(studentID = studentid)

    # Serialize attendance data
    serializer = StudentAttendance(student_sheet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def presence_types(request):
    try:
        if request.method == 'GET':
            queryset = Presence.objects.order_by('id')
            serializer = PresenceSerializer(queryset, many=True)
            return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)