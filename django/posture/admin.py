from django.contrib import admin
from .models import correction_video

class videoadmin(admin.ModelAdmin) :
    list_display = ('video_index','posture','video_link')

    search_fields =  ('posture',)
    ordering = ('posture',)

    filter_horizontal = ()

admin.site.register(correction_video, videoadmin) #site에 등록
