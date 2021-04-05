from django.urls import path, include
# from django.contrib.auth import views as auth_views
from system import views

app_name = 'system'

urlpatterns = [
    # user Authentication
    path('', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),


    # # CRUD
    # path('createuser/', views.createEmployee, name='createEmployee'),
    # path('find/', views.find, name='find'),
    # path('update/<slug:p_id>', views.updateEmployee, name='updateEmployee'),
    # path('destroy/<slug:p_id>', views.destroy, name='destroy'),
    # # APIs
    # path('employeeslist/', views.employees_list, name='employeeslist'),
    # path('updatesalary/<slug:p_id>/<int:value>', views.update_salary, name='updatesalary'),
    # path('listbyname/<slug:name>', views.list_by_name, name='listbyname'),
    # path('deletebygender/<slug:gender>', views.delete_by_gender, name='deletebtgender'),
]