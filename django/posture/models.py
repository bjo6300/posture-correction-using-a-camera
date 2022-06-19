from django.db import models


class correction_video(models.Model):
    video_index = models.AutoField(verbose_name='게시글 인덱스', primary_key=True)
    posture = models.CharField(max_length=100, verbose_name='자세 이름')
    title = models.CharField(max_length=200, verbose_name='제목')
    video_link = models.CharField(max_length=1000, verbose_name='영상 주소')

    def __str__(self):
        return self.posture

    class Meta:
        db_table = 'correction_video'
    
