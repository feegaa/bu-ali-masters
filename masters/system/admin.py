from django.contrib import admin
from system.models import User, College, Orientation, Group

admin.site.register(College)
admin.site.register(Group)
admin.site.register(Orientation)
admin.site.register(User)