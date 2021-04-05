from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path('jury/', views.juryRequest, name='jury_request'),
    path('disserta/', views.disserta, name='disserta'),
    path('create/dissertation/', views.dissertationCreate, name='create_dissertation'),
    path('report/dissertation/', views.dissertationReport, name='dissertation_report'),
    path('report/dissertation/edit/', views.dissertationReportEdit, name='dissertation_report_edit'),
    path('report/achievement/', views.achievementReport, name='achievement_report'),    
    path('report/achievement/edit/', views.achievementReportEdit, name='achievement_report_edit'), 
    path('<str:username>/', views.dashboard, name='dashboard'),
]
