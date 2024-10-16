from django.urls import path
from home import views
from .views import studentattendance,studentresult
from .views import take_test, test_result
from django.conf.urls import handler404
from home.views import custom_404_view
urlpatterns = [
    
    path('',views.index,name="home"),
    path('login',views.Login_page,name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('user',views.Sign_up,name='user'),
    path('userprofile',views.userPage,name='userprofile'),
    path('studentuser',views.student_user,name='studentuser'),
    path('student',views.studentprofile,name='student'),
    path('teachers/<str:username>/',views.teacher,name='teachers'),
    path('studentdetails',views.studentdetail,name='studentdetails'),
    path('teacherdetails',views.teacherdetail,name='teacherdetails'),
    path('courses',views.course,name='courses'),
    path('attendances',views.attendance,name='attendances'),
    path('grades',views.grade,name='grades'),
    path('addstudents',views.addstudent, name = 'addstudents'),
    path('example',views.example,name='example'),
    path('addcourses',views.addcourse,name='addcourses'),
    path('subjects',views.subjectt,name='subjects'),
    path ('sessions',views.session,name='sessions'),
    path('grade_list',views.grade_lists,name= 'grade_list'),
    path('attendancereport',views.report,name='attendancereport'),
    path('studentprofile',views.sprofile, name='studentprofile'),
    path('delete/<int:rollid>', views.deleterecord, name = 'delete'),
    path('delete/<int:id>', views.Coursedelete, name = 'delete'),
    path('student_attendance/', studentattendance, {'report_type': 'all'}, name='student_attendance_all'),
    path('student_attendance/<str:report_type>/', studentattendance, name='student_attendance'),
    path('attendance_details/',views.attendancedetails, {'report_type': 'all'}, name='attendance_details_all'),
    path('attendance_details/<str:report_type>/', views.attendancedetails, name='attendance_details'),
    path('editstudent/<str:username>/',views.editstudentrecord, name='editstudent'),
    path('editteacher/<str:username>/',views.editteacherrecord, name='editteacher'),
    path('teacherprofile',views.tprofile, name='teacherprofile'),
    path('teachermenu',views.teacher_menu,name = 'teachermenu'),
    path('reportview/',views.report_view, {'report_type': 'all'}, name='reportview_all'),
    path('reportview/<str:report_type>/',views.report_view, name='reportview'),
    path('result',views.s_result, name='result'),
    path('student_result/<int:student_id>/', views.studentresult, name='student_result'),
    path('student_result/', views.no_student, name='no_student'),
     # Teacher URLs
    path('createtest/', views.create_test, name='create_test'),  # Teachers create a test
    path('add-questions/<int:test_id>/', views.add_questions, name='add_questions'),  # Teachers add questions to a test
    
    # Student URLs
    path('test/<int:test_id>/', take_test, name='take_test'),
    path('result/<int:result_id>/', test_result, name='test_result'), # Students take a test and submit answers
    path('tests/', views.test_list, name='test_list'),  # List all tests
    path('studentmenu',views.smenu,name='studentmenu'),

   

   
]


handler404 = custom_404_view