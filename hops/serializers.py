from django.contrib.auth.models import Group, User
from rest_framework import serializers
from hops.models import ClassGroups, Students, AttendanceSheet, Presence, AttendanceRecord

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupsSerializer(serializers.BaseSerializer):
    class Meta:
        model = ClassGroups
        fields = ['groupName']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.groupName
        }


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id','name']


class GroupSerializer(serializers.ModelSerializer):
    members = GroupsSerializer(many=True, read_only=True)


    class Meta:
        model = ClassGroups
        fields = ['id', 'groupName', 'members']

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ['id', 'title']

class AttendanceRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['studentID', 'presenceID']
        depth = 1

class AttendanceSerializer(serializers.ModelSerializer):
    name_list = AttendanceRecordsSerializer(many=True, read_only=True)
    class Meta:
        model = AttendanceSheet
        fields = ['date', 'group','name_list']


class StudentAttendance(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['presenceID', 'sheetID']
        depth = 1