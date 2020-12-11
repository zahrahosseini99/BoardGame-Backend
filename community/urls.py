from django.urls import path
from . import views


urlpatterns = [
    path('create_community/', views.CreateCommunityView.as_view()),
]
