from django.urls import path
from . import views

urlpatterns = [
    path('create_cafe/', views.CreateCafeView.as_view()),
    path('search_cafe/name/', views.SearchCafeView.as_view()),
]
