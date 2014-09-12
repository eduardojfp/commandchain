from django.contrib import admin
from chain_of_command.models import *
# Register your models here.
admin.site.register(Member)
admin.site.register(Hierarchy)
admin.site.register(Post)
admin.site.register(Position)
admin.site.register(Organization)
admin.site.register(Message)
admin.site.register(Order)