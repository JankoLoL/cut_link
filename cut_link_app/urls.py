from django.urls import path
from .views import RegisterView, UrlSubmitView, HomePageView, CustomLoginView, UrlRedirectView, UrlDeleteView, \
    UrlDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(next_page='home'), name='login'),
    path('submit-url/', UrlSubmitView.as_view(), name='submit_url'),
    path('', HomePageView.as_view(), name='home'),
    path('<str:shortened_id>/', UrlRedirectView.as_view(), name='url_redirect'),
    path('url-detail/<int:pk>/', UrlDetailView.as_view(), name='url_detail'),
    path('delete/<int:pk>/', UrlDeleteView.as_view(), name='url_delete'),

]
