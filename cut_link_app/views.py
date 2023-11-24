from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView

from .forms import RegisterForm, UrlSubmitForm


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'


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


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
