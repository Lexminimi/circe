from django.db import models
from django.contrib.postgres.fields import ArrayField


class Students(models.Model):
    '''
    Student names
    '''
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(models.User)
    classes = ArrayField(ArrayField(models.IntegerField()))

class ClassGroups(models.Model):
    '''
    Group names - for example beginner class A,B - you can have multiple classes a week wich belongs to one group
    '''
    groupname = models.CharField(max_length=100)

class Classes(models.Model):
    '''
    Class object
    '''
    teacher = models.ForeignKey(models.User)
    name = models.CharField(max_length=100)
    days = models.IntegerField()
    hour = models.TimeField(auto_now=False, auto_now_add=False)
    classgroup = models.ForeignKey(models.Classes)