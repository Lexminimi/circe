from django.db import models
from django.contrib.auth.models import User


def teacher_default():
    user = User.objects.order_by('id').first()
    if user:
        return user.id
    else:
        return 1


class Students(models.Model):
    '''
    Student names
    '''
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default = teacher_default())


class ClassGroups(models.Model):
    '''
    Group names - for example beginner class A,B - you can have multiple classes a week wich belongs to one group
    '''
    groupName = models.CharField(max_length=100)
    members = models.ManyToManyField(Students)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default = teacher_default())


class Presence(models.Model):
    ''' Model for different presence type verified absence, unverified absence, present'''
    title = models.CharField(max_length = 100)

class Attendance(models.Model):
    '''
    Log the attendance for a class
    '''
    date = models.DateTimeField("date published")
    #serializer_class = ClassSerializer
    #http_method_names = ['post']
    group = models.ForeignKey(ClassGroups, on_delete = models.CASCADE)
    studentID = models.ForeignKey(Students, on_delete = models.CASCADE)
    presence = models.ForeignKey(Presence, on_delete = models.CASCADE)