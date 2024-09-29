from django.http import HttpResponse

from .models import Students, ClassGroups
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import AttendanceForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hops.serializers import GroupSerializer, UserSerializer, ClassGroupSerializer


@api_view(['GET'])
def classgroup_list(request):
    try:
        group = ClassGroups.objects.all()
        serializer = GroupSerializer(group, many=True)
        print(serializer)
        return Response(serializer.data)
    except ClassGroups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def classgroup_detail(request, pk):
    group = ClassGroups.objects.get(pk  = pk)
    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

class GroupStudentsView(viewsets.ModelViewSet):
    """
    Retrieve students belonging to a specific group
    """
    def rertrieve(self, pk):
        queryset = ClassGroups.objects.all()
        serializer_class = get_object_or_404(queryset, pk=pk)
        permission_classes = [permissions.AllowAny]
        return Response(serializer_class.data)

    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk = None):
        queryset =  ClassGroups.objects.all()
        group = get_object_or_404(queryset, pk=pk).members.all()
        serializer_class = ClassGroupSerializer(group)
        permission_classes = [permissions.AllowAny]



def index(request):
    students_list = Students.objects.order_by("name")[:5]
    output = ", ".join([q.name for q in students_list])
    return HttpResponse(output)

def trainingGroups(request):
    try:
        # Fetch the ClassGroups instance with the provided ID
        group = ClassGroups.objects.filter()


    except ClassGroups.DoesNotExist:
        # Handle the case where the group ID is invalid
        context = {'error_message': 'Group not found!'}
        return "No result"

    # Render the template with the list of student names
    return render(request, 'classes.html', {'classes': group})


def AttendanceSheet(request, group_id):
    """
       Lists all Students.name belonging to a specific ClassGroups instance.

       Args:
           request (HttpRequest): The Django HTTP request object.
           group_id (int): The ID of the ClassGroups instance to retrieve members for.

       Returns:
           HttpResponse: A Django response object with the rendered template
               containing the list of student names.
       """

    try:
        # Fetch the ClassGroups instance with the provided ID
        group = get_object_or_404(ClassGroups, pk=group_id)

    except ClassGroups.DoesNotExist:
        # Handle the case where the group ID is invalid
        context = {'error_message': 'Group not found!'}
        return "No result"

    # Render the template with the list of student names
    return render(request, 'presence.html', {'students': group.members.all()})

def groupMembers(request, group_id):
    """
    Lists all Students.name belonging to a specific ClassGroups instance.

    Args:
        request (HttpRequest): The Django HTTP request object.
        group_id (int): The ID of the ClassGroups instance to retrieve members for.

    Returns:
        HttpResponse: A Django response object with the rendered template
            containing the list of student names.
    """

    try:
        # Fetch the ClassGroups instance with the provided ID
        group = ClassGroups.objects.get(pk=group_id)
    except ClassGroups.DoesNotExist:
        # Handle the case where the group ID is invalid
        context = {'error_message': 'Group not found!'}
        return "No result"

    # Retrieve all Students belonging to the group using ManyToManyField
    members = group.members.all()


    # Render the template with the list of student names
    output = ", ".join([q.name for q in members])
    return HttpResponse(output)

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AttendanceForm()

    return render(request, "name.html", {"form": form})
