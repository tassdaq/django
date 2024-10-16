from django.urls import resolve
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from home.models import Studentprofile,Teacherprofile,Course,Session,Subject,Grade,Attendance,AttendanceReport,Test, Question, Choice, StudentResult
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import date
from django.db import IntegrityError
from .forms import SubjectForm,AttendanceForm,StudentForm,TeacherForm,GradeForm,SessionForm,CourseForm,AttendancereportForm,UpdateUserForm,UpdateStudentForm,UpdateTeacherForm, ChoiceForm
from .forms import TestCreationForm  
from .forms import StudentTestForm
from .forms import QuestionCreationForm, ChoiceFormSet

# Create your views here.


@login_required(login_url='login')
@admin_only
def index(request):
    studentss = Studentprofile.objects.all().count()
    teacher = Teacherprofile.objects.all().count()
    c = Course.objects.all().count()
    data = Attendance.objects.all()
    sub = Subject.objects.all().count()



    return render(request,'base.html',{'studentss' : studentss , 'teacher' : teacher ,'c':c, 'data':data, 'sub':sub})

@unauthenticated_user
def Login_page(request):
    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('home')
            
            else:
                messages.info(request,'Username OR password is incorrect')
        context ={}
        return render(request,'login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def Sign_up(request):
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user= form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='teacher')
                user.groups.add(group)
                Teacherprofile.objects.create(user=user,)

                messages.success(request,'Account was created for' + username)
                return redirect('login') 
            
        context = {'form':form}
        return render(request,'user.html', context)
    

def userPage(request):
    
    
    return render(request,'userprofile.html')    

@login_required
def teacher_menu(request):
    tp = Teacherprofile.objects.all()
    total = Teacherprofile.objects.all().count()
    sub = Subject.objects.all().count()
    c = Course.objects.all().count()
    total_students = AttendanceReport.objects.count()
    present_students = AttendanceReport.objects.filter(status=True).count()
    absent_students = total_students - present_students

    context = {
        'total_students': total_students,
        'present_students': present_students,
        'absent_students': absent_students,
        'sub':sub,
        'total':total,
        'c':c,
        'tp':tp

    }
    return render(request,'teachermenu.html',context)


def report_view(request,report_type = 'all'):
    tp = Teacherprofile.objects.all()
    if report_type == 'present':
        reports = AttendanceReport.objects.filter(status=True)
    elif report_type == 'absent':
        reports = AttendanceReport.objects.filter(status=False)
    
    else:
        reports = AttendanceReport.objects.filter()
    return render(request,'reportview.html',{'reports': reports, 'report_type': report_type,'tp':tp})




def tprofile(request): 
    user = request.user

    if request.method == 'POST':
        teacher_profile_form = TeacherForm(request.POST, request.FILES)

        if  teacher_profile_form.is_valid():
            teacher_profile = teacher_profile_form.save(commit=False)
            teacher_profile.user = user
            teacher_profile.save()
            return redirect('teachermenu')  # Redirect to the teacherprofile view after creating

    else:
        user_form = UpdateUserForm(instance=user)
        teacher_profile_form = TeacherForm()

    context = {
        'user_form': user_form,
        'teacher_profile_form': teacher_profile_form,
    }
     
    return render(request,'teacherprofile.html',context)


    
@unauthenticated_user
def student_user(request):
     form = CreateUserForm()

     if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user= form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='student')
                user.groups.add(group)
                Studentprofile.objects.create(user=user,)

                messages.success(request,'Account was created for' + username)
                return redirect('login') 
            
     context = {'form':form}
     return render(request,'studentuser.html', context)
     
     
def studentattendance(request,report_type = 'all'):
    sp = Studentprofile.objects.all()
    student = request.user.studentprofile
    if report_type == 'present':
        reports = AttendanceReport.objects.filter(student = student,status=True)
    elif report_type == 'absent':
        reports = AttendanceReport.objects.filter(student = student,status=False)
    
    else:
        reports = AttendanceReport.objects.filter(student=student)
    return render(request,'student_attendance.html',{'reports': reports, 'report_type': report_type,'sp':sp})


def studentprofile(request):
    pro = Studentprofile.objects.filter(user = request.user)
    context = {'pro':pro}
    return render(request,"student.html",context)

def attendancedetails(request,report_type):
    if report_type == 'present':
        reports = AttendanceReport.objects.filter(status=True)
    elif report_type == 'absent':
        reports = AttendanceReport.objects.filter(status=False)
    elif report_type == 'all':
        reports = AttendanceReport.objects.all()
    else:
    # Handle invalid report_type, you can customize this based on your needs
        return render(request, 'error_page.html', {'error_message': 'Invalid report type'})
    return render(request,'attendance_details.html',{'reports': reports, 'report_type': report_type})


def sprofile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        student_profile_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_profile_form.is_valid():
            user_form.save()
            student_profile = student_profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()
            return redirect('student')  # Redirect to the studentprofile view after creating

    else:
        user_form = UpdateUserForm(instance=user)
        student_profile_form = StudentForm()

    context = {
        'user_form': user_form,
        'student_profile_form': student_profile_form,
    }

    return render(request, 'studentprofile.html', context)

def teacher(request):
     return render(request,("teachers.html"))

def studentdetail(request):
     st = Studentprofile.objects.all()
     context = {'st' : st}
     return render(request,'studentdetails.html',context)

def deleterecord(request, rollid):
    form = Studentprofile.objects.get(rollid= rollid)    
    form.delete()
    return redirect("/studentdetails")

def Coursedelete(request, id):
    form = Course.objects.get(id= id)    
    form.delete()
    return redirect("/courses")


def teacherdetail(request):
     teacherss = Teacherprofile.objects.all()
     context = {'t':teacherss}
     return render(request,'teacherdetails.html',context)


def addcourse(request):
     if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addcourses')  # Redirect to a success page or another view
     else:
        form = CourseForm()
        
     return render(request,'addcourses.html',{'form':form})

def attendance(request):
     if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendances')  # Redirect to a success page or another view
     else:
        form = AttendanceForm()

     return render(request, 'attendances.html', {'form': form})

@admin_only
def grade(request):
     if request.method == 'POST':
      form = GradeForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('grade_list')
     else:
      form = GradeForm()
     return render(request,'grades.html',{'form' : form})

@login_required
def addstudent(request):
     profile = get_object_or_404(Studentprofile, user=request.user)
     if request.method == 'POST':
        form = StudentForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('studentdetails')
     else:
        form = StudentForm(instance=profile)

     return render(request,'addstudents.html', {'form': form})


def editstudentrecord(request,username):
    sp = Studentprofile.objects.all()
    user = get_object_or_404(User, username=username)
    student_profiles = Studentprofile.objects.filter(user=user)

    if student_profiles.exists():
        # Choose how to handle multiple profiles, for now, taking the first one
        student_profile = student_profiles.first()

        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=user)
            student_profile_form = UpdateStudentForm(request.POST, request.FILES, instance=student_profile)
            if user_form.is_valid() and student_profile_form.is_valid():
                user_form.save()
                student_profile_form.save()
                messages.success(request,"Updated Successfully")
                return redirect('studentmenu')  # Redirect to the studentprofile view after updating
                
        else:
            user_form = UpdateUserForm(instance=user)
            student_profile_form = UpdateStudentForm(instance=student_profile)

        context = {
            'user_form': user_form,
            'student_profile_form': student_profile_form,
            'sp':sp
        }

        return render(request, 'editstudent.html', context)
    else:
        # Handle the case where no profile is found
        return render(request, 'profile_not_found.html')
    


def editteacherrecord(request,username):
    tp = Teacherprofile.objects.all()
    user = get_object_or_404(User, username=username)
    teacher_profiles = Teacherprofile.objects.filter(user=user)

    if teacher_profiles.exists():
        # Choose how to handle multiple profiles, for now, taking the first one
        teacher_profile = teacher_profiles.first()

        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=user)
            teacher_profile_form = UpdateTeacherForm(request.POST, request.FILES, instance=teacher_profile)
            if user_form.is_valid() and teacher_profile_form.is_valid():
                user_form.save()
                teacher_profile_form.save()
                messages.success(request,"Updated Successfully")
                return redirect('teachermenu')  # Redirect to the studentprofile view after updating
                
        else:
            user_form = UpdateUserForm(instance=user)
            teacher_profile_form = UpdateTeacherForm(instance=teacher_profile)

        context = {
            'user_form': user_form,
            'teacher_profile_form': teacher_profile_form,
            'tp':tp
        }

        return render(request, 'editteacher.html', context)
    else:
        # Handle the case where no profile is found
        return render(request, 'profile_not_found.html')
    

def example(request):
    s = Studentprofile.objects.all().count()
    t = Teacherprofile.objects.all().count()

    return render(request,'example.html',{'s':s, 't':t})

def course(request):
     cc= Course.objects.all()
     context = {'cc':cc}
     return render(request,'courses.html',context)

def subjectt(request):  
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects')  # Redirect to a success page or another view
    else:
        form = SubjectForm()

    return render(request, 'subjects.html', {'form': form})

def session(request):
     if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sessions')  # Redirect to a success page or another view
     else:
        form = SessionForm()
      
     return render(request,'sessions.html',{'form':form})



def grade_lists(request):
    grade = Grade.objects.all()
    return render(request, 'grade_list.html', {'grades': grade})


def report(request):
    tp = Teacherprofile.objects.all()
    if request.method == 'POST':
        form = AttendancereportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachermenu')  # Redirect to a success page or another view
    else:
        form = AttendancereportForm()
    return render(request,'attendancereport.html',{'form': form,'tp':tp})



def s_result(request):
    tp = Teacherprofile.objects.all()
    if request.method == 'POST':
      form = GradeForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('teachermenu')
    else:
      form = GradeForm()
    return render(request,'result.html',{'form':form,'tp':tp})


def studentresult(request, student_id):
    sp = Studentprofile.objects.all()
    print(f"Received Student ID: {student_id}")  # Debugging output
    
    # Fetch the student profile
    student = get_object_or_404(Studentprofile, id=student_id)
    print(f"Found Student: {student.user.username}")  # Debugging output

    # Fetch grades for the student
    grades = Grade.objects.filter(student=student)
    print(f"Grades found: {grades}")  # Debugging output

    return render(request, 'student_result.html', {'student': student, 'grades': grades,'sp':sp})


def no_student(request):
    sp = Studentprofile.objects.all()
    return render(request, 'no_student.html',{'sp':sp})



def create_test(request):
    tp = Teacherprofile.objects.all()
    try:
        teacher_profile = Teacherprofile.objects.get(user=request.user)
    except Teacherprofile.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        test_form = TestCreationForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.created_by = teacher_profile  # Set the teacher who created the test
            test.save()  # Save the test instance

            # Add selected students to the test
            students_ids = request.POST.getlist('students')  # Assuming you use a multiple select for students
            test.students.set(students_ids)

            return redirect('add_questions', test_id=test.id)  # Redirect to add questions
    else:
        test_form = TestCreationForm()  # Render an empty form for GET request

    return render(request, 'create_test.html', {'form': test_form, 'tp': tp})


def add_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()

    if request.method == 'POST':
        question_form = QuestionCreationForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()

            for choice_form in choice_formset:
                if choice_form.cleaned_data:
                    choice_instance = choice_form.save(commit=False)
                    choice_instance.question = question
                    choice_instance.save()

            return redirect('add_questions', test_id=test.id)
    else:
        question_form = QuestionCreationForm()
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())

    context = {
        'test': test,
        'questions': questions,
        'question_form': question_form,
        'choice_formset': choice_formset
    }

    return render(request, 'add_questions.html', context)

def test_list(request):
    try:
        student_profile = Studentprofile.objects.get(user=request.user)
        # Filter tests associated with the logged-in student
        tested = Test.objects.filter(students=student_profile)
    except Studentprofile.DoesNotExist:
        return redirect('home')  # Redirect if the student profile does not exist

    return render(request, 'test_list.html', {'tested': tested})


def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    try:
        student_profile = Studentprofile.objects.get(user=request.user)
        # Ensure the test belongs to the student's course
        if test.created_by.course != student_profile.course:
            return redirect('test_list')
    except Studentprofile.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        score = 0
        total_questions = test.questions.count()
        selected_choices_dict = {}

        for question in test.questions.all():
            selected_choices = request.POST.getlist(f'question_{question.id}')
            selected_choices_dict[question.id] = selected_choices

            for choice_id in selected_choices:
                if question.choices.get(id=choice_id).is_correct:
                    score += 1

        result = StudentResult(
            student=student_profile,
            test=test,
            score=(score / total_questions) * 100 if total_questions > 0 else 0
        )
        result.save()

        request.session['selected_choices'] = selected_choices_dict
        return redirect('test_result', result_id=result.id)

    else:
        form = StudentTestForm(test)

    return render(request, 'take_test.html', {'test': test})

def test_result(request, result_id):
    sp = Studentprofile.objects.all()
    result = get_object_or_404(StudentResult, id=result_id)
    questions = result.test.questions.all()

    correct_choices = {choice.id for question in questions for choice in question.choices.all() if choice.is_correct}
    selected_choices = request.session.get('selected_choices', [])

    return render(request, 'test_result.html', {
        'result': result,
        'correct_choices': correct_choices,
        'selected_choices': selected_choices,
        'questions': questions,
        'sp': sp
    })


def smenu(request):
    sp = Studentprofile.objects.filter(user=request.user)
    return render(request,'studentmenu.html',{'sp':sp})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)    




 
    


   



