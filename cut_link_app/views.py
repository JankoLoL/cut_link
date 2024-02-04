from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, DeleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login

from .forms import RegisterForm, UrlSubmitForm
from .models import ShortenedUrl


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        if user.is_active:
            login(self.request, user)
            return redirect('home')
        else:
            return redirect('login')


class UrlSubmitView(LoginRequiredMixin, FormView):
    form_class = UrlSubmitForm
    template_name = 'url_submit.html'
    success_url = reverse_lazy('url_list')

    def form_valid(self, form):
        shortened_url = form.save(commit=False)
        shortened_url.user = self.request.user
        shortened_url.save()
        return super().form_valid(form)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UrlSubmitForm()
        context['shortened_urls'] = ShortenedUrl.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = UrlSubmitForm(request.POST)
        if form.is_valid():
            shortened_url = form.save(commit=False)
            shortened_url.user = request.user
            shortened_url.save()
            return redirect('url_detail', pk=shortened_url.pk)
        return self.render_to_response(self.get_context_data(form=form))


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class UrlDetailView(DetailView, LoginRequiredMixin):
    model = ShortenedUrl
    template_name = 'url_detail.html'
    context_object_name = 'shortened_url'


class UrlRedirectView(View, LoginRequiredMixin):
    def get(self, request, shortened_id):
        url = get_object_or_404(ShortenedUrl, shortened_id=shortened_id)
        return redirect(url.original_url)


class UrlDeleteView(LoginRequiredMixin, DeleteView):
    model = ShortenedUrl
    success_url = reverse_lazy('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
