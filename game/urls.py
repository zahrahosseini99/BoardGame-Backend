from django.urls import path
from . import views


urlpatterns = [
    path('game_info/<int:pk>/', views.GameInfoPageView.as_view()),
    path('hot_games/', views.HotnessGamesListView.as_view()),
    path('games_list/',views.GamesListView.as_view()),
]
