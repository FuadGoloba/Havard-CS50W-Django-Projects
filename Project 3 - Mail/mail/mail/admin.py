from django.contrib import admin

# Register your models here.

from .models import Email, User

class EmailAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'subject', 'body', 'timestamp', 'read', 'archived']

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email', 'username']

admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)