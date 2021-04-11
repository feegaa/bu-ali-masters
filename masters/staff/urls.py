from django.urls import path
from staff import views

app_name = 'staff'

urlpatterns = [
    path('add/professor/', views.addProfessor, name='add_professor'),
    path('add/student/', views.addStudent, name='add_student'),
    path('add/group/', views.addGroup, name='add_group'),
    path('set/group/admin/<int:id>', views.setGroupAdmin, name='set_group_admin'),
    path('add/orientation/', views.addOrientation, name='add_orientation'),
    path('groups/', views.groups, name='groups'),
    path('professor/list/<int:id>/', views.groups, name='group_professor_list'),
    path('student/list/<int:id>/', views.groups, name='group_student_list'),
    path('error/', views.error, name='error'),
    path('group/<int:id>/edit/', views.editGroup, name='edit_group'),
    path('group/<int:id>/delete/', views.deleteGroup, name='delete_group'),
    path('<str:username>/', views.dashboard, name='dashboard'),
]
