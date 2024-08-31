from django.db import models
from django.contrib.auth.models import User


def teacher_default():
    return User.objects.order_by('id').first().id


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

class Classes(models.Model):
    '''
    Class object
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default = teacher_default())
    name = models.CharField(max_length=100)
    days = models.IntegerField()
    hour = models.TimeField(auto_now=False, auto_now_add=False)
    classGroup = models.ForeignKey(ClassGroups, on_delete=models.CASCADE)


class Attendance(models.Model):
    '''
    Log the attendance for a class
    '''
    date = models.DateTimeField("date published")
    group = models.ForeignKey(ClassGroups, on_delete = models.CASCADE)