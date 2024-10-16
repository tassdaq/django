from django.contrib import admin
from .models import Studentprofile,Teacherprofile,Subject,Course,Attendance,AttendanceReport,Session,Grade,Test,Choice,StudentResult,Question
# Register your models here.
admin.site.register(Studentprofile)
admin.site.register(Teacherprofile)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Session)
admin.site.register(Grade)
admin.site.register(Test)
admin.site.register(Choice)
admin.site.register(StudentResult)
admin.site.register(Question)



admin.site.site_header="HYSEC ADMIN"
admin.site.site_title="HYSEC ADMIN PORTAL"
admin.site.index_title="Welcome to Hysec Admin Portal"
