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
            'name': instance.name
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

class StudentWithPresenceSerializer(serializers.ModelSerializer):
    presence = serializers.SerializerMethodField()

    class Meta:
        model = Students
        fields = ['id', 'name', 'presence']

    def get_presence(self, student):
        attendance = self.context.get('attendance')
        # Fetch presence record for this student and attendance
        presence_record = Presence.objects.filter(attendance=attendance)
        return presence_record.id if presence_record else None

class AttendanceSerializer(serializers.ModelSerializer):
    groupid = serializers.IntegerField(source='group.id')
    date = serializers.DateTimeField()
    sheetID = AttendanceSheet.get(date)

    class Meta:
        model = AttendanceSheet
        fields = ['groupid', 'date', 'students']

    def get_students(self, attendance):
        students = attendance.students.all()
        return StudentWithPresenceSerializer(
            students, many=True, context={'attendance': attendance}
        ).data