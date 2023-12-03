from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import create_user
urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html", next_page="/"), name='login-view'),
    path('logout/', LogoutView.as_view(next_page="/"), name="logout-view"),
    path('register/', create_user, name="register-user"),
    path('', include('django.contrib.auth.urls'))
]
