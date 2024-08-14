from django.contrib.auth.models import User
from django.db import models


class SearchHistory(models.Model):
    """
    검색 기록
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='사용자')
    url = models.URLField(max_length=200, blank=True, null=True,
                          verbose_name='URL')
    text_input = models.TextField(blank=True, null=True, verbose_name='텍스트 입력')
    file_name = models.CharField(max_length=200, blank=True, null=True,
                                 verbose_name='파일 이름')
    summary_result = models.TextField(blank=True, null=True,
                                      verbose_name='영어 요약 결과')
    translation_result = models.TextField(blank=True, null=True,
                                          verbose_name='한글 번역 결과')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    def __str__(self):
        return f"Search by {self.user.username} on {self.created_at}"
