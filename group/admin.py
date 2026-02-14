from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(AllUser)
admin.site.register(Group)
admin.site.register(Messages)
admin.site.register(SecureGroup)
admin.site.register(SecureMessages)