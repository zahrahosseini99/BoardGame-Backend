from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('edit_profile/', views.EditProfileView.as_view(), name='auth_edit_profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='auth_change_password'),
]
