from datetime import datetime
from django.http import HttpResponse

from .models import Students, ClassGroups, Attendance, Presence

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import AttendanceForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hops.serializers import GroupSerializer, UserSerializer, ClassGroupSerializer, GroupsSerializer, AttendenceSerializer


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

@api_view(['POST'])
def attendence_create(request, pk):
    if request.method == 'POST':
        serializer = AttendenceSerializer(data=request.data)
        # Get current date
        today = datetime.today()
        logger.info(f"Today's date: {today}")
        # Check if attendance for today and the group already exists
        if Attendance.objects.filter(date=today, group=pk).exists():
            return Response({"message": "Attendance for this group already exists today."})
        # Retrieve all students in the group
        group_students = Students.objects.filter(classgroups = pk)

        # Create attendance for each student
        for student in group_students:
            Attendance.objects.create(
                date=today,
                group = ClassGroups(id=pk) ,
                studentID=student,
                presence=Presence(1)  # default to False or however you track presence
            )

        return Response({"message": "New attendance sheet created for today."}, status=status.HTTP_201_CREATED)




