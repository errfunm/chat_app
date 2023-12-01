from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html", next_page="/"), name='login-view'),
    path('logout/', LogoutView.as_view(next_page="login/"), name="logout-view"),
]
