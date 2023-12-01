from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views 
from .views import DeleteQuestion, QuizComment, QuizCreate, QuizFeed, QuizEdit, QuestionCreate, Questions

urlpatterns = [
    path('', views.index, name="index"),
    path("<int:i>/", views.quiz, name="quiz"),
    path('<int:i>/data/', views.quiz_data_view, name="quiz-data"),
    path('<int:i>/save/', views.save_quiz_view, name="quiz-save"),

    path('register/', views.register, name="register"),
    #path('logout', views.logout, name="logout"),

    path('quizcreate/', QuizCreate.as_view(), name="quizcreate"),
    path('quizquestions/<int:pk>/',Questions.as_view(), name="quizquestions"),
    path('quizquestions/<int:pk>/quizaddquestion/', login_required(QuestionCreate.as_view()), name="quizaddquestion"),

    path('quizedit/<int:pk>/', login_required(QuizEdit.as_view()), name="quizedits"),
    path('quizoptionadd/<int:pk>/', views.quiz_option_add, name="quizoption"), 
    #path('quizoptionadd/<int:pk>/', QuestionAnswers.as_view(), name="quizoption"), 
    path('quizdeletequestion/<int:pk>/', login_required(DeleteQuestion.as_view()), name="quizdeletequestion"),

    path('like/<int:pk>', views.like_view, name="quizlikes"),
    path('quizfeed/<int:pk>/', QuizFeed.as_view(), name="quizfeed"),
    path('quizfeed/<int:pk>/quizaddcomments/', login_required(QuizComment.as_view()), name="quizaddcomments"),
    path('searches/', views.quiz_searches, name="searches"),
]