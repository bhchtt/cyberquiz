from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'awareness'

urlpatterns = [
    path('', views.home, name='home'),
    path('theory/', views.theory, name='theory'),
    path('contacts/', views.contacts, name='contacts'),

    path('quiz/start/', views.quiz_start, name='quiz_start'),
    path('quiz/question/', views.quiz_question, name='quiz_question'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result_detail, name='quiz_result_detail'),
    path('results/', views.results, name='results'),

    path('login/', auth_views.LoginView.as_view(template_name='awareness/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
]
