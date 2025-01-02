from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView




app_name = 'users'
urlpatterns = [
    #include default auth urls.
    path('',include('django.contrib.auth.urls')),
    # Registration page.
    path('register/',views.register,name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]