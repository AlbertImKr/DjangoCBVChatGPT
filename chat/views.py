from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ChatForm
from .utils import generate_prompt
from .utils import get_completion
from .utils import translate_to_korean


class ChatView(LoginRequiredMixin, FormView):
    template_name = 'chat/index.html'
    form_class = ChatForm
    success_url = '/'

    def form_valid(self, form):
        text_input = form.cleaned_data.get('text_input')
        file_input = form.cleaned_data.get('file_input')
        youtube_url = form.cleaned_data.get('youtube_url')
        prompt = generate_prompt(text_input, file_input, youtube_url)
        summary_result = get_completion(prompt)

        translation_result = translate_to_korean(summary_result)
        return self.render_to_response(
                self.get_context_data(
                        summary_result=summary_result,
                        translation_result=translation_result,
                )
        )


class HomeView(TemplateView):
    template_name = 'chat/home.html'
