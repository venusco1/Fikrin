from django.urls import path
from . import views

app_name = 'FknAp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms_and_conditions, name='terms'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path("n/createpost", views.create_post, name="create_post"),
]
