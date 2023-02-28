from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [

    path('registration/', views.registartion, name="registration"),
    path("login/", views.user_login, name="user_login"),
]