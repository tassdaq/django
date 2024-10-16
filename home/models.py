from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField(default=now)

    def __str__(self):
        return self.name

class Session(models.Model):
    start_year = models.DateField(default=now)
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)

g = (('Male', 'Male'), ('Female', 'Female'))

class Studentprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    rollid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=300, null=True)
    gender = models.CharField(max_length=50, choices=g, default="Male")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=False)  # Change to SET_NULL
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)  # Change to SET_NULL
    photo = models.ImageField(null=True) 
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.user)

class Teacherprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=300, null=True)
    gender = models.CharField(max_length=50, choices=g, default="Male") 
    phone = models.CharField(max_length=50, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=False)  # Change to SET_NULL  
    photo = models.ImageField(null=True) 
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.user)

class Subject(models.Model):
    name = models.CharField(max_length=120)
    teacheruser = models.ForeignKey(Teacherprofile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=now)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # Change to CASCADE if you want to keep it
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.session)

class AttendanceReport(models.Model):
    student = models.ForeignKey(Studentprofile, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.student.user.first_name)

class Grade(models.Model):
    student = models.ForeignKey(Studentprofile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.user}'s Grade in {self.subject.name}"

# Test model to hold each test created by a teacher
class Test(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(Teacherprofile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Studentprofile, blank=True)  # Add this line

    def __str__(self):
        return self.title

# Question model for each question within a test
class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.test.title}"

# Choice model for each answer option in a question
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

# Model to store the student's test result
class StudentResult(models.Model):
    student = models.ForeignKey(Studentprofile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)  
