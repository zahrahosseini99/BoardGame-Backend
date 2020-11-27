from django.urls import path
from . import views


urlpatterns = [
    path('game_info/<int:pk>/', views.GameInfoPageView.as_view()),
    path('hot_games/', views.HotnessGamesListView.as_view()),
    path('difficult_games/', views.DifficultGamesListView.as_view()),
    path('games_list/',views.GamesListView.as_view()),
    path('search_user/username/', views.SearchUserView.as_view()),
    path('search_game/name/', views.SearchGameView.as_view()),
    path('create_play/', views.CreatePlayView.as_view()),
    path('plays_list/', views.PlaysListView.as_view()),
    path('owner_plays_list/', views.OwnerPlaysListView.as_view()),
    path('edit_play/<int:pk>/', views.EditPlayView.as_view()),
]
