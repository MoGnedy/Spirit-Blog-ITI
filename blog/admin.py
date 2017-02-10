from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category , Post , Reply ,ForbiddenWords
# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name' ,'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_superuser')
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(ForbiddenWords)