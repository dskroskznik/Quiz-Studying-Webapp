from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from .models import QuizModel, QuestionModel, AnswerModel, QuizComments, User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizModel
        fields = ['name', 'descriptor', 'timelimit']

class QuestionForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea, label='')
    hint = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'value': 'no hint'}))
    class Meta:
        model = QuestionModel
        fields = ['info',]
        widgets = {
            'quiz': forms.TextInput(attrs={'class': 'form-control', 'id': 'question'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = '__all__'

class QuizCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = QuizComments
        fields = ['body',]
        widgets = {
            'quiz': forms.TextInput(attrs={'class': 'form-control', 'id': 'comm'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
        }