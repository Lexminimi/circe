from django.http import HttpResponse

from .models import Students, ClassGroups

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import AttendanceForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hops.serializers import GroupSerializer, UserSerializer, ClassGroupSerializer, GroupsSerializer


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




