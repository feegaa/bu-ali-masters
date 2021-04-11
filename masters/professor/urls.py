from django.urls import path
from professor import views

app_name = "professor"

urlpatterns = [
    path('request/master/', views.masterRequest, name='request_master'),
    path('request/supervise/', views.superviseRequest, name='request_supervise'),
    path('jury/invite/', views.juryInvite, name='jury_invite'),
    path('<str:username>/', views.dashboard, name='dashboard'),
]
