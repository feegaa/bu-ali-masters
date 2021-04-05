from django.db import models
from django.contrib.auth.models import BaseUserManager
from system.models import User, College

class Staff(User):
    class Meta:
        proxy = True

    class StaffManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(item_type=User.Types.STAFF)

    def save(self, *args, **kwargs):
        self.item_type = User.Types.STAFF
        self.is_staff  = True
        return super().save(*args, **kwargs)

    objects = StaffManager()

    @property
    def fields(self):
        return self.stafffields

class StaffFields(models.Model):
    college = models.ForeignKey(College, on_delete=models.DO_NOTHING)
    staff   = models.OneToOneField(Staff, on_delete=models.CASCADE)
