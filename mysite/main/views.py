from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.db import transaction
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import AnswerForm, QuestionForm, QuizForm, RegisterForm, QuizCommentForm
from .models import QuizComments, QuizModel, QuestionModel, AnswerModel, QuizResults
# Create your views here.

def index(req):
    if req.method == 'POST':
        quiz_d = req.POST.get('quizdelete')
        delete = QuizModel.objects.filter(id=quiz_d).first()
        if delete and delete.author == req.user:
            delete.delete()

    quizzes = QuizModel.objects.all()
    
    return render(req, 'index.html', {"quizzes": quizzes})

def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)       
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(req, 'registration/register.html', {"form": form})

#@login_required(login_url="/login")
#def quiz_create(req):
    if req.method == 'POST':
        form = QuizForm(req.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = req.user
            quiz.save()
            return redirect('/quizaddquestion')
    else:
        form = QuizForm()
    return render (req, 'quizcreate.html', {"form": form})    

class QuizCreate(LoginRequiredMixin, CreateView):
    model = QuizModel
    form_class = QuizForm
    template_name = 'quizcreate.html'
    login_url = '/login'
    redirect_field_name = '/'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class QuizEdit(LoginRequiredMixin, UpdateView):
    model = QuizModel
    form_class = QuizForm
    template_name = 'quizedit.html'
    login_url = '/login'
    redirect_field_name = '/'


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = QuestionModel
    form_class = QuestionForm
    template_name = 'quizaddquestion.html' 
    login_url = '/login'
    redirect_field_name = '/'
    #fields = ('name', 'descriptor', 'timelimit')'
    
    def form_valid(self,form):
        form.instance.quiz_id = self.kwargs['pk']
        return super().form_valid(form)

class Questions(ListView):
    model = QuestionModel
    template_name = 'quizquestions.html'

class QuizFeed(DetailView):
    model = QuizModel
    template_name = 'quizfeed.html'
    
#   -- Dated Function Logic for posting question answers --    
#class QuestionAnswers(LoginRequiredMixin, CreateView):
#    model = AnswerModel
#    form_class = AnswerForm
#    template_name = 'quizoptionadd.html'
#    success_url = "/quizquestions/{quiz_id}"
#    login_url = '/login'
#    redirect_field_name = '/'

#    def form_valid(self,pk):
#        question = QuestionModel.objects.get(id=pk)        
#        QuestionFormSet = inlineformset_factory(QuestionModel, AnswerModel, fields=('info','correct_ans', 'question'), extra=4)
#        if self.request.method=="POST":
#            formset = QuestionFormSet(self.request.POST, instance=question)
#            if formset.is_valid():
#                formset.save()
#                return super(QuestionAnswers, self).form_valid(formset)
#        else:
#            formset=QuestionFormSet(instance=question)
#        return render(self.request, 'quizoptionadd.html', {"formset": formset, "question": question})
    
class QuizComment(LoginRequiredMixin, CreateView):
    model = QuizComments
    form_class = QuizCommentForm
    template_name = 'quizaddcomment.html'
    login_url = '/login'
    redirect_field_name = '/'
    success_url = "/quizfeed/{quiz_id}"

    def form_valid(self,form):
        form.instance.quiz_id = self.kwargs['pk']
        form.instance.name = self.request.user.username
        return super().form_valid(form)
        return reverse('quizfeed', args=(str(self.id)))

class DeleteQuestion(LoginRequiredMixin, DeleteView):
    model = QuestionModel
    template_name = 'quizdeletequestion.html'
    success_url = "/quizquestions/{quiz_id}"
    login_url = '/login'
    redirect_field_name = '/'

@login_required(login_url="/login")
def quiz(req, i):
    quiz = QuizModel.objects.get(id=i)
    return render(req, 'quiz.html', {"quiz": quiz})

#   -- Previous method before Classes to establishing quizzes form and data --
#def quiz_comments(req, i):
    quizid = QuizModel.objects.get(id=i)
    form = QuizCommentForm(instance=quizid)
    if req.method == 'POST':
        form = QuizCommentForm(req.POST, instance=quizid)
        if form.is_valid():
            newcomment = form.save(commit=False)
            newcomment.save()
            return redirect('/quizaddquestion')
    else:
        form = QuizCommentForm()
    return render(req, "quizcomments.html", {'form': form, 'quizid': quizid})

#def quiz_add_comments(req, i):
    quizid = QuizModel.objects.get(id=i)
    form = QuizCommentForm(instance=quizid)
    if req.method == 'POST':
        form = QuizCommentForm(req.POST, instance=quizid)
        if form.is_valid():
            newcomment = form.save(commit=False)
            newcomment.save()
            return render(req, 'searches.html', {'form': form, 'quizid': quizid},)
    else:
        form = QuizCommentForm()
    return render(req, "quizcomments.html", {'form': form, 'quizid': quizid})

#def quiz_questions(req):
    questions = QuestionModel.objects.all()
    questions = QuestionModel.objects.filter().order_by('-id')
    
    return render(req, 'quizquestions.html', {"questions": questions})

#def quiz_edit(req, i):
    quizedit = QuizModel.objects.get(id=i)
    form = QuizForm(instance=quizedit)
    if req.method == 'POST':
        form = QuizForm(req.POST or None, instance=quizedit)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = req.user
            return redirect('quizaddquestion')
    else:
        form = QuizForm(instance=quizedit)
    return render(req, 'quizedit.html', {"quizedit": quizedit, "form": form})   

def quiz_option_add(req, pk):
    question = QuestionModel.objects.get(id=pk)       
    QuestionFormSet = inlineformset_factory(QuestionModel, AnswerModel, fields=('info','correct_ans', 'question'), extra=4)
    if req.method=="POST":
        formset = QuestionFormSet(req.POST, instance=question)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('quizquestions', args=[question.quiz.id]))
    else:
        formset=QuestionFormSet(instance=question)
    return render(req, 'quizoptionadd.html', {"formset": formset, "question": question})

def quiz_data_view(req, i):
    quiz = QuizModel.objects.get(id=i)
    questions = []
    for q in quiz.get_questionmodels():
        answers = []
        for a in q.get_answermodels():
            answers.append(a.info)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.timelimit,
    })

def is_ajax(req):
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_quiz_view(req, i):
    if is_ajax(req=req):
        questions = []
        data = req.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = QuestionModel.objects.get(info=k)
            questions.append(question)

        user = req.user
        quiz = QuizModel.objects.get(id=i)
        
        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            selected = req.POST.get(q.info)

            if selected != "":
                question_answers = AnswerModel.objects.filter(question=q)
                for a in question_answers:
                    if selected == a.info:
                        if a.correct_ans:
                            score += 1
                            correct_answer = a.info
                    else:
                        if a.correct_ans:
                            correct_answer = a.info

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        QuizResults.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    
def quiz_searches(req):
    if req.method == 'POST':
        search = req.POST['search']
        quizsearch = QuizModel.objects.filter(name__icontains=search)
        return render(req, 'searches.html', {'search': search, 'quizsearch': quizsearch},)
    else:
        return render(req, 'searches.html',)
    
def like_view(req, pk):
    qlikes = get_object_or_404(QuizModel, id=req.POST.get('quizlikes'))
    qlikes.likes.add(req.user)
    return HttpResponseRedirect(reverse('index'))