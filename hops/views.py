from datetime import datetime
from django.http import HttpResponse

from .models import Students, ClassGroups, AttendanceSheet, Presence, AttendanceRecord

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import AttendanceForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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

@api_view(['POST', 'GET'])
def attendance( request, group_id, date=None):
    if request.method == 'GET':
        # Retrieve attendance record by group and date
        attendance_sheet = get_object_or_404(AttendanceSheet, group_id = group_id, date = date)

        # Serialize attendance data
        serializer = AttendanceSerializer(attendance_sheet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        logger.warning("Platform is running at risk POST")
        today = datetime.today().date()

        # Check if attendance for today and the group already exists
        if Attendance.objects.filter(date__date=today, group_id=group_id).exists():
            return Response({"message": "Attendance for this group already exists today."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the group and its students
        group = get_object_or_404(ClassGroups, id=group_id)
        students_in_group = group.members.all()

        # Create a new attendance record for each student in the group
        attendance = Attendance.objects.create(date=today, group=group)
        logger.info("Creation called")
        attendance.students.set(students_in_group)  # Link all group students to the attendance record

        # Set default presence for each student as needed
        # (e.g., mark as "absent" initially or customize based on your logic)

        # Serialize the created attendance data
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def student_attendance( request, studentid):
    student_sheet = AttendanceRecord.objects.filter(studentID = studentid)

    # Serialize attendance data
    serializer = StudentAttendance(student_sheet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)