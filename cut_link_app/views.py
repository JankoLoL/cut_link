from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import RegisterForm, UrlSubmitForm


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class UrlSubmitView(LoginRequiredMixin, FormView):
    form_class = UrlSubmitForm
    template_name = 'url_submit.html'
    success_url = reverse_lazy('url_list')

    def form_valid(self, form):
        shortened_url = form.save(commit=False)
        shortened_url.user = self.request.user
        shortened_url.save()
        return super().form_valid(form)


class HomePageView(TemplateView):
    template_name = 'home.html'
