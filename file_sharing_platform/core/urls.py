from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard    , name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]