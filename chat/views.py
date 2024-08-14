from django.conf import settings
from django.views.generic.edit import FormView
from openai import OpenAI
from django import forms

from .forms import ChatForm

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        chat_completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5,
        )
        forms.Form.clean()
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


class ChatView(FormView):
    template_name = 'chat/index.html'
    form_class = ChatForm
    success_url = '/'

    def form_valid(self, form):
        user_input = form.cleaned_data['user_input']
        result = get_completion(user_input)
        return self.render_to_response(
                self.get_context_data(form=form, result=result)
        )

