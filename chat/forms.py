from django import forms


class ChatForm(forms.Form):
    user_input = forms.CharField(
            label='사용자 입력창',
            max_length=100,
            widget=forms.TextInput(
                    attrs={'class': 'form-control',
                           'placeholder': '무엇을 도와드릴까요?',
                           }
            )
    )
