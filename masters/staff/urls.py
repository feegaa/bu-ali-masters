from django.urls import path
from staff import views, professorView, studentView

app_name = 'staff'

urlpatterns = [
    # PROFESSOR CRUD
    path('add/professor/', professorView.addProfessor, name='add_professor'),
    path('professors/', professorView.addProfessor, name='professor_list'),
    path('professor/<int:id>/edit/', professorView.professorEdit, name='professor_edit'),
    
    # STUDENT CRUD
    path('student/<int:id>/edit/', studentView.studentEdit, name='student_edit'),
    path('add/student/', studentView.addStudent, name='add_student'),
    path('students/', studentView.addStudent, name='student_list'),
    
    # SYSTEM CRUD
    path('add/group/', views.addGroup, name='add_group'),
    path('group/admin/<int:id>', views.setGroupAdmin, name='set_group_admin'),
    path('add/orientation/', views.addOrientation, name='add_orientation'),
    path('group/<int:id>/edit/', views.editGroup, name='edit_group'),
    path('group/<int:id>/delete/', views.error, name='delete_group'),
    path('orientation/<int:id>/edit/', views.editOrientation, name='edit_orientation'),
    path('orientation/<int:id>/delete/', views.deleteOrientation, name='delete_orientation'),
    
    # GET
    path('groups/', views.groups, name='groups'),
    path('group/<int:id>/orientations/', views.groupOrientationList, name='group_orientation_list'),
    path('group/<int:id>/professors/', views.groups, name='group_professor_list'),
    path('group/<int:id>/students/', views.groups, name='group_student_list'),
    path('orientation/<int:id>/students/', views.groups, name='orientation_student_list'),
    path('error/', views.error, name='error'),
    path('<str:username>/', views.dashboard, name='dashboard'),
]
