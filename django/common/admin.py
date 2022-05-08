from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin) :
    list_display = ('user_id','gender','user_email','birth')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('user_id', 'user_password')}),
        ('Personal info', {'fields': ('gender', 'user_email','birth')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields =  ('user_id',)
    ordering = ('user_id','user_email')

    filter_horizontal = ()


admin.site.register(User, UserAdmin) #site에 등록
