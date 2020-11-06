from django.urls import path
from . import views


urlpatterns = [
    path('game_info/<int:pk>/', views.GameInfoPageView.as_view()),
]
