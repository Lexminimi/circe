from datetime import datetime
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema

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

@swagger_auto_schema()
@api_view(['GET'])
def classgroup_list(request):
    """
    List all class groups.
    
    Returns a list of all class groups in the system.
    """
    try:
        if request.method == 'GET':
            queryset = ClassGroups.objects.order_by('id')
            serializer = GroupsSerializer(queryset, many=True)
            return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def classgroup_detail(request, pk):
    """
    Retrieve a specific class group.
    
    Returns detailed information about a specific class group, including its members.
    """
    group = ClassGroups.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = GroupDetailSerializer(group)
        return Response(serializer.data)

import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
@csrf_exempt
def attendance( request, group_id, date=None):
    """
    Get or create attendance records for a class group on a specific date.
    
    GET: Retrieve attendance records for the specified group and date.
    """
    if request.method == 'GET':
        # Retrieve attendance record by group and date
        attendance_sheet = get_object_or_404(AttendanceSheet, group_id = group_id, date = date)

        # Serialize attendance data
        serializer = AttendanceSerializer(attendance_sheet)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_attendance_sheet(request, group_id):
    """
    Create a new attendance sheet for a class group.
    
    Creates a new attendance sheet for today's date and initializes attendance records for all members.
    """
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
    """
    Get attendance records for a specific student.
    
    Returns all attendance records for the specified student.
    """
    student_sheet = AttendanceRecord.objects.filter(studentID = studentid)

    # Serialize attendance data
    serializer = StudentAttendance(student_sheet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def presence_types(request):
    """
    List all presence types.
    
    Returns a list of all possible presence types (e.g., Present, Absent, etc.).
    """
    try:
        if request.method == 'GET':
            queryset = Presence.objects.order_by('id')
            serializer = PresenceSerializer(queryset, many=True)
            return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def attendance_update(request, groupID, studentID,attendType, date = None):
    """
    Update a student's attendance status.
    
    Updates the attendance status for a specific student in a specific group on a specific date.
    """
    if request.method == 'POST':
        # Use today's date dynamically if no date is provided
        if date == None:
            current_date = datetime.now().date().strftime('%Y-%m-%d')

        s = AttendanceSheet.objects.get(date = current_date, group_id = groupID)

        if AttendanceSheet.objects.filter(date = current_date, group_id = groupID).exists():
            # Retrieve attendance record by group and date
            student_attendance = get_object_or_404(AttendanceRecord, sheetID = s, studentID = studentID )
            student_attendance.presenceID = Presence.objects.get(id=attendType)
            student_attendance.save()
            # Serialize attendance data
            serializer = StudentAttendance(student_attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def teacher_groups(request, teacher_id):
    """
    List all class groups for a specific teacher.
    
    Returns all class groups and their members for the specified teacher.
    """
    try:
        if request.method == 'GET':
            queryset = ClassGroups.objects.filter(teacher_id=teacher_id).order_by('id')
            serializer = GroupDetailSerializer(queryset, many=True)
            return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)