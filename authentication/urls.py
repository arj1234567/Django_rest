from django.urls import include, path
from authentication import views

urlpatterns = [
    path('login', views.LoginApiView.as_view()),
    path('logout',views.LogoutApiView.as_view()),
    
]