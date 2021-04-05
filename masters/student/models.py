from django.db import models
from django.contrib.auth.models import BaseUserManager
from system.models import User, Group, Orientation
from django_jalali.db import models as jmodels

class Student(User):
    class Meta:
        proxy = True

    class StudentManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(item_type=User.Types.STUDENT)

    def save(self, *args, **kwargs):
        self.item_type = User.Types.STUDENT
        return super().save(*args, **kwargs)

    objects = StudentManager()

    @property
    def fields(self):
        return self.studentfields

class StudentFields(models.Model):
    student      = models.OneToOneField(Student, on_delete=models.CASCADE)
    entry_at     = models.DateField(auto_now_add=True)
    is_graduated = models.BooleanField(default=False)
    is_daily     = models.BooleanField(default=True)
    describtion  = models.CharField(max_length=300, blank=True)
    
    # RELATIONS
    group        = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    orientation  = models.ForeignKey(Orientation, on_delete=models.DO_NOTHING)



class Dissertation(models.Model):
    title       = models.CharField(max_length=500)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at  = jmodels.jDateTimeField(auto_now_add=True)
    jury_date   = jmodels.jDateField()
    objects     = jmodels.jManager() 

    # RELATIONS
    student     = models.OneToOneField(Student, on_delete=models.CASCADE)



class AchievementReport(models.Model):
    class Status(models.IntegerChoices):
       REJECTED    = 0 
       ACCEPTED    = 1
       IN_PROGRESS = 2

    grade_average    = models.JSONField()
    status           = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    report_id        = models.CharField(max_length=20, blank=True)
    created_at       = models.DateField(auto_now_add=True)
    supervisor_ok    = models.BooleanField(default=False)
    manager_ok       = models.BooleanField(default=False)
    supervisor_quote = models.CharField(max_length=400, blank=True)
    manager_quote    = models.CharField(max_length=400, blank=True)
    objects          = models.Manager() 
    
    # RELATIONS
    student          = models.ForeignKey(Student, on_delete=models.CASCADE)
    disserta         = models.ForeignKey(to='DissertationReport', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'disserta'], name='report')
        ]

class DissertationReport(models.Model):
    title            = models.CharField(max_length=400, blank=False)
    summary          = models.CharField(max_length=500)
    problems         = models.CharField(max_length=500)
    proceedings      = models.CharField(max_length=500)
    created_at       = models.DateField(auto_now_add=True)
    supervisor_ok    = models.BooleanField(default=False)
    manager_ok       = models.BooleanField(default=False)
    supervisor_quote = models.CharField(max_length=400, blank=True)
    manager_quote    = models.CharField(max_length=400, blank=True)
    objects          = models.Manager() 

    # RELATIONS
    disserta         = models.ForeignKey(Dissertation, on_delete=models.CASCADE)




class JuryRequest(models.Model):
    class Status(models.IntegerChoices):
       REJECTED    = 0 
       ACCEPTED    = 1
       IN_PROGRESS = 2
    status           = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    jury_date        = models.DateField()
    created_at       = models.DateField(auto_now_add=True)
    supervisor_ok    = models.BooleanField(default=False)
    supervisor_quote = models.CharField(max_length=400, blank=True)
    manager_ok       = models.BooleanField(default=False)
    manager_quote    = models.CharField(max_length=400, blank=True)
    staff_ok         = models.BooleanField(default=False)   
    staff_quote      = models.CharField(max_length=400, blank=True)
    objects          = models.Manager()
    
    # RELATIONS
    dissertation     = models.OneToOneField(Dissertation, on_delete=models.CASCADE)
    student          = models.OneToOneField(Student, on_delete=models.CASCADE)
