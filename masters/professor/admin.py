from django.contrib import admin
from professor.models import Professor, ProfessorFields

admin.site.register(Professor)
admin.site.register(ProfessorFields)
# Register your models here.