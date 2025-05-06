from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('select/', views.select_view, name='select'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_view, name='create'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('code/', views.code_view, name='code'),
    path('folder/<str:folder_name>/', views.custom_view, name='custom'),  
    path('quiz/<str:folder_name>/', views.custom_quiz_view, name='custom_quiz'),
    path('quiz/save/', views.save_quiz, name='save_quiz'),
    path('generate_questions/', views.generate_questions, name='generate_questions'),
]
    





