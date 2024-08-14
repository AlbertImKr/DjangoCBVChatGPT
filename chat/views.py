from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import ChatForm
from .models import SearchHistory
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

        SearchHistory.objects.create(
                user=self.request.user,
                url=youtube_url,
                text_input=text_input,
                file_name=file_input.name if file_input else None,
                summary_result=summary_result,
                translation_result=translation_result,
        )

        return self.render_to_response(
                self.get_context_data(
                        summary_result=summary_result,
                        translation_result=translation_result,
                )
        )


class SearchHistoryView(LoginRequiredMixin, ListView):
    model = SearchHistory
    template_name = 'chat/search_history.html'
    context_object_name = 'search_histories'

    def get_queryset(self):
        return (SearchHistory.objects.filter(user=self.request.user)
                .order_by('-created_at'))

class HomeView(TemplateView):
    template_name = 'chat/home.html'
