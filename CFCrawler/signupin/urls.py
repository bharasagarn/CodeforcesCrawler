from django.conf.urls import url
from signupin import views
from django.urls import path

app_name = 'signupin'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
]