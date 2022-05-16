from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin) :
    list_display = ('username','gender','email','birth')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('gender', 'email','birth')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields =  ('username',)
    ordering = ('username',)

    filter_horizontal = ()
    

admin.site.register(User, UserAdmin) #site에 등록
