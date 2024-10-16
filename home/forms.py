from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms 
from .models import Subject,Attendance,Studentprofile,Teacherprofile,Grade,Session,Course,AttendanceReport,Test,Question,StudentResult,Choice
from django.forms import modelformset_factory



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']     
        widgets ={
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),

        }   


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacheruser','course','date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'teacheruser': forms.Select(attrs={'class':'form-control'}),
            'course': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['start_year','end_year']
        widgets = {
            'start_year': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'end_year': forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
      model = Course
      fields = ['name','date']   
      widgets = {
           'name': forms.TextInput(attrs={'class':'form-control'}),
           'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
       }      


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['session','subject','date']  
        widgets = {
            'session': forms.Select(attrs={'class':'form-control'}),
            'subject': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Studentprofile
        fields = ['address','gender','photo']  
        widgets = {
          
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'gender' : forms.Select(attrs={'class':'form-control'}),
            'photo': forms.FileInput(attrs={'class':'form-control'}),
        }

class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Studentprofile
        fields = ['address','photo']
        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'photo': forms.FileInput(attrs={'class':'form-control'}),
        }



class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacherprofile
        fields = ['address','gender','phone','photo']                  
        widgets = {
            
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'photo':forms.FileInput(attrs={'class':'form-control'}),
            
        }

class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacherprofile
        fields = ['address','phone','photo']                  
        widgets = {
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'photo':forms.FileInput(attrs={'class':'form-control'}),
           
        }        

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value',]
        widgets = {
            'student': forms.Select(attrs={'class':'form-control'}),
            'subject': forms.Select(attrs={'class':'form-control'}),
            'value': forms.NumberInput(attrs={'class':'form-control'}),

        }


class AttendancereportForm(forms.ModelForm):
    class Meta:
        model =  AttendanceReport
        fields = ['student','attendance','status','date']
        widgets = {
            'student': forms.Select(attrs={'class':'form-control'}),
            'attendance': forms.Select(attrs={'class':'form-control'}),
            'status': forms.CheckboxInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }       

        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']


  


        

class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']       


ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=4)        


class TestCreationForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Studentprofile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Test
        fields = ['title', 'students']  # Include students field


# This form is for displaying existing questions with multiple choices
class QuestionChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)  # Get the questions from kwargs
        super().__init__(*args, **kwargs)

        if questions:
            for question in questions:
                choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=choices, widget=forms.RadioSelect, label=question.question_text
                )

class StudentTestForm(forms.Form):
    def __init__(self, test, *args, **kwargs):
        super(StudentTestForm, self).__init__(*args, **kwargs)
        for question in test.questions.all():
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                label=question.question_text,
                choices=choices,
                widget=forms.CheckboxSelectMultiple
            )
