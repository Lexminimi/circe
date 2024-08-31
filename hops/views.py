from django.http import HttpResponse

from .models import Students, ClassGroups


def index(request):
    students_list = Students.objects.order_by("name")[:5]
    output = ", ".join([q.name for q in students_list])
    return HttpResponse(output)

def trainingGroups(request):
    classes = ClassGroups.objects.order_by("groupName")
    output = ", ".join([q.groupName for q in classes])
    return HttpResponse(output)

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
