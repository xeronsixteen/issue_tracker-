from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UsersView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('users/', UsersView.as_view(), name='UsersView')

]
