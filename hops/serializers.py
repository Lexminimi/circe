from django.contrib.auth.models import Group, User
from rest_framework import serializers
from hops.models import ClassGroups, Students, Attendance

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

class ClassGroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(source='students.all', many=True, read_only=True)  # Include students in the response

    class Meta:
        model = ClassGroups
        fields = ['id', 'groupName', 'members']

class GroupSerializer(serializers.ModelSerializer):
    members = StudentSerializer(many=True, read_only=True)


    class Meta:
        model = ClassGroups
        fields = ['id', 'groupName', 'members']

class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'group', 'studentID', 'presence']

    def create(self, validated_data):
        """
        Create and return a new `Attendance` instance, given the validated data.
        """
        return Attendance.objects.create(**validated_data)