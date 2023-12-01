from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuizModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text="Quiz Name (50 Character Limit)")
    descriptor = models.CharField(max_length=500,help_text="Quiz Description")
    timelimit = models.IntegerField(default=1, null=True, help_text="Quiz Duration in seconds")
    questions = models.IntegerField(default=1, null=True)
    likes = models.ManyToManyField(User, related_name="quizblock")

    def __str__(self):
        return self.name + "\n"
    def get_absolute_url(self):
        return reverse('quizquestions', kwargs={'pk':self.id})
    def get_questionmodels(self):    
        return self.questionmodel_set.all()
    def total_likes(self):
        return self.likes.count()

class QuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    info = models.CharField(max_length=300, help_text="What Is The Question?")
    hint = models.CharField(max_length=300, help_text="Provide An Optional Hint For The Question", null=True)

    def __str__(self):
        return self.info
    def get_absolute_url(self):
        return reverse('quizquestions', kwargs={'pk':self.quiz_id})
    def get_answermodels(self): 
        return self.answermodel_set.all()
    
class AnswerModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    info = models.CharField(max_length=300)
    correct_ans = models.BooleanField(default=False)

    def __str__(self):
        return f"question: {self.question.info}, answer: {self.info}, {self.correct_ans}"
    def get_absolute_url(self):
        return reverse('quizquestions', kwargs={'pk':self.quiz_id})
    
class QuizResults(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.quiz)
    
class QuizComments(models.Model):
    quiz = models.ForeignKey(QuizModel, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.quiz.name, self.body)