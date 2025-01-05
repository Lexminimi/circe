import os
import django
from faker import Faker
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'circe.circe.settings')  # Replace 'your_project.settings' with your actual settings module
django.setup()

from django.contrib.auth.models import User
from circe.hops.models import Students, ClassGroups, Presence, AttendanceSheet, AttendanceRecord  # Replace 'your_app' with your app name

fake = Faker()

# Create fake teachers (Users)
teachers = []
for _ in range(5):  # Adjust the number of teachers
    user = User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password="password123"
    )
    teachers.append(user)

# Create Presence types
presence_types = ["Present", "Verified Absence", "Unverified Absence"]
presence_objects = []
for title in presence_types:
    presence = Presence.objects.create(title=title)
    presence_objects.append(presence)

# Create Students and ClassGroups
students = []
class_groups = []

for teacher in teachers:
    # Create students for each teacher
    for _ in range(10):  # Adjust the number of students per teacher
        student = Students.objects.create(name=fake.name(), teacher=teacher)
        students.append(student)

    # Create class groups
    for _ in range(2):  # Adjust the number of groups per teacher
        group = ClassGroups.objects.create(
            groupName=fake.word().capitalize() + " Group",
            teacher=teacher
        )
        group.members.set(random.sample(students, k=random.randint(5, 10)))  # Assign random students to the group
        class_groups.append(group)

# Create Attendance Sheets
attendance_sheets = []
for group in class_groups:
    for _ in range(5):  # Adjust the number of attendance sheets per group
        sheet = AttendanceSheet.objects.create(
            date=fake.date_time_this_year(),
            group=group
        )
        attendance_sheets.append(sheet)

# Create Attendance Records
for sheet in attendance_sheets:
    for student in sheet.group.members.all():
        AttendanceRecord.objects.create(
            sheetID=sheet,
            studentID=student,
            presenceID=random.choice(presence_objects)
        )

print("Data populated successfully!")
