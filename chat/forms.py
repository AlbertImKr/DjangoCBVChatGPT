from django import forms


class ChatForm(forms.Form):
    text_input = forms.CharField(
            label='글 내용 요약',
            max_length=1000,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '요약할 내용을 입력하세요...',
                'rows': 4,
            }),
            required=False
    )
    file_input = forms.FileField(
            label='PDF 파일 업로드',
            widget=forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            required=False
    )
    youtube_url = forms.URLField(
            label='유튜브 URL',
            widget=forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '유튜브 URL을 입력하세요...',
            }),
            required=False
    )
