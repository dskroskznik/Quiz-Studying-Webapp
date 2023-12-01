from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.QuizModel)
admin.site.register(models.QuestionModel)
admin.site.register(models.AnswerModel)
admin.site.register(models.QuizResults)
admin.site.register(models.QuizComments)