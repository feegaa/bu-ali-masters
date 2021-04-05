from django.db import models
from django.contrib.auth.models import BaseUserManager
from system.models import User, Group, Orientation

class Professor(User):
    class Meta:
        proxy = True

    class ProfessorManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(item_type=User.Types.PROFESSOR)

    def save(self, *args, **kwargs):
        self.item_type = User.Types.PROFESSOR
        return super().save(*args, **kwargs)


    objects = ProfessorManager()

    @property
    def fields(self):
        return self.professorfields

class ProfessorFields(models.Model):

    class Grades(models.TextChoices):
        INSTRUCTOR = 0
        ASSISTANT  = 1
        ASSOCIATE  = 2
        PROFESSOR  = 3

    professor       = models.OneToOneField(Professor, on_delete=models.CASCADE)
    is_adminstrator = models.BooleanField(default=False)
    grade           = models.CharField(max_length=10, choices=Grades.choices)
    last_university = models.CharField(max_length=100)

    # RELATIONS
    group           = models.ForeignKey(Group, on_delete=models.DO_NOTHING)


class PHDRequest(models.Model):
    class Status(models.IntegerChoices):
       REJECTED    = 0 
       ACCEPTED    = 1
       IN_PROGRESS = 2

    request_id = models.CharField(max_length=10, blank=True)
    status     = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    clause_a   = models.JSONField()
    clause_b   = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    manager_ok = models.BooleanField(default=False)
    staff_ok   = models.BooleanField(default=False)
    objects    = models.Manager() 
    
    # RELATIONS
    professor  = models.ForeignKey(Professor, on_delete=models.CASCADE)

class MasterRequest(models.Model):
    class Status(models.IntegerChoices):
       REJECTED    = 0 
       ACCEPTED    = 1
       IN_PROGRESS = 2

    request_id  = models.CharField(max_length=10, blank=True)
    status      = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    type_1      = models.SmallIntegerField()
    type_2      = models.SmallIntegerField()
    created_at  = models.DateField(auto_now_add=True)
    manager_ok  = models.BooleanField(default=False)
    staff_ok    = models.BooleanField(default=False)
    objects     = models.Manager() 

    # RELATIONS
    orientation = models.ForeignKey(Orientation, on_delete=models.DO_NOTHING)
    professor   = models.ForeignKey(Professor, on_delete=models.DO_NOTHING)
