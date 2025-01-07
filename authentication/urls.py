from django.urls import include, path
from authentication import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login', views.LoginApiView.as_view()),
    path('logout',views.LogoutApiView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]