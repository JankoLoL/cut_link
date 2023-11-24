
from django.urls import path
from .views import RegisterView, UrlSubmitView, HomePageView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', RegisterView.as_view(), name='login'),
    path('submit-url/', UrlSubmitView.as_view(), name='submit_url'),
    path('', HomePageView.as_view(), name='home'),
]
