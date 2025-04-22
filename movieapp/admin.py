from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Genre)
admin.site.register(Movies)
admin.site.register(PasswordReset)
admin.site.register(Profile)