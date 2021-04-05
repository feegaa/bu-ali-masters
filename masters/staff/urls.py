from django.urls import path
from staff import views

app_name = 'staff'

urlpatterns = [
    path('add/professor/', views.addProfessor, name='add_professor'),
    path('add/student/', views.addStudent, name='add_student'),
    path('add/group/', views.addGroup, name='add_group'),
    path('add/orientation/', views.addOrientation, name='add_orientation'),
    path('groups/', views.groups, name='groups'),
    path('error/', views.error, name='error'),
    path('<str:username>/', views.dashboard, name='dashboard'),
]
