from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField 

class College(models.Model):
    title   = models.CharField(max_length=100, unique=True)
    objects = models.Manager() 


class Group(models.Model):
    title   = models.CharField(max_length=100, unique=True)
    objects = models.Manager() 
    
    # RELATIONS
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    @property
    def adminstrator(self):
        return self.adminstrator

class Adminstrator(models.Model):
    professor = models.ForeignKey(to='professor.Professor', on_delete=models.DO_NOTHING)
    group     = models.OneToOneField(Group, primary_key=True, on_delete=models.CASCADE)

class Orientation(models.Model):
    title   = models.CharField(max_length=100, unique=True)
    objects = models.Manager() 
    
    # RELATIONS
    group   = models.ForeignKey(Group, on_delete=models.CASCADE)

class User(AbstractUser):
    
    class Gender(models.IntegerChoices):
        FEMALE = 0
        MALE   = 1
        NONE   = 2
    
    class Types(models.IntegerChoices):
        STUDENT   = 0
        PROFESSOR = 1
        STAFF     = 2
        OTHER     = 3

    first_name = models.CharField(max_length=30, blank=False)
    last_name  = models.CharField(max_length=30, blank=False)
    password   = models.CharField(max_length=100, blank=False)
    email      = models.EmailField(unique=True)
    username   = models.CharField(unique=True, max_length=10)
    n_code     = models.CharField(unique=True, max_length=10)
    phone      = PhoneNumberField(blank=False)
    item_type  = models.IntegerField(choices=Types.choices, default=Types.OTHER)
    is_staff   = models.BooleanField(default=False)
    gender     = models.IntegerField(choices=Gender.choices, default=Gender.NONE)
    created_at = models.DateField(auto_now_add=True, blank=True)
    is_active  = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['n_code']

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_password(self.n_code)
        else:
            self.set_password(self.password)
            
        return super().save(*args, **kwargs)



class JuryInvitation(models.Model):
    class Status(models.IntegerChoices):
       REJECTED    = 0 
       ACCEPTED    = 1
       IN_PROGRESS = 2
    status     = models.IntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    created_at = models.DateField(auto_now_add=True)
    jury_date  = models.DateField()
    objects    = models.Manager()
    
    # RELATIONS
    professor  = models.ForeignKey(to="professor.Professor", on_delete=models.DO_NOTHING)
    disserta   = models.ForeignKey(to='student.Dissertation', on_delete=models.DO_NOTHING)


class Supervisor(models.Model):
    class Percent(models.IntegerChoices):
        Q1   = 25
        HALF = 50
        Q3   = 75
        FULL = 100
    student   = models.ForeignKey(to="student.Student", on_delete=models.DO_NOTHING, related_name="student")
    professor = models.ForeignKey(to="professor.Professor", on_delete=models.DO_NOTHING, related_name="professor")
    percent   = models.IntegerField(choices=Percent.choices, default=Percent.FULL)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'professor'], name="supervisor")
        ]
  
