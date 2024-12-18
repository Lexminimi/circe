from django.db import models
from django.contrib.auth.models import User




class Students(models.Model):
    '''
    Student names
    '''
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class ClassGroups(models.Model):
    '''
    Group names - for example beginner class A,B - you can have multiple classes a week wich belongs to one group
    '''
    groupName = models.CharField(max_length=100)
    members = models.ManyToManyField(Students)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.groupName


class Presence(models.Model):
    ''' Model for different presence type verified absence, unverified absence, present'''
    title = models.CharField(max_length = 100)
    def __str__(self):
        return self.title


class AttendanceSheet(models.Model):
    '''
    Log the attendance for a class
    '''
    date = models.DateTimeField("date published")
    group = models.ForeignKey(ClassGroups, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.date.date()) + ' ' + self.group.groupName


class AttendanceRecord(models.Model):
    """
        Tracks attendance for each student within a specific attendance sheet.
        """
    sheetID = models.ForeignKey(AttendanceSheet, related_name='name_list', on_delete=models.CASCADE)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    presenceID = models.ForeignKey(Presence, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sheetID.date.date()) + ' ' + self.studentID.name
