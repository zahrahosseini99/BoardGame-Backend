from django.urls import path
from . import views


urlpatterns = [
    path('create_community/', views.CreateCommunityView.as_view()),
    path('community_info/<int:pk>/', views.CommunityInfoPageView.as_view()),
]
