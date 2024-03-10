from django.urls import path
from . import views
from .views import gallery_view, set_profile_pic

app_name = 'Authentication'

urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms_and_conditions, name='terms'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('gallery/', gallery_view, name='gallery'),
    path('set_profile_pic/<int:image_id>/', set_profile_pic, name='set_profile_pic'),
    path('about/',views.about_us, name='about-us'),
    path('save-token/', views.save_token, name='save_token'),
]


