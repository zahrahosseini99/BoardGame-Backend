from django.urls import path
from . import views

urlpatterns = [
    path('create_cafe/', views.CreateCafeView.as_view()),
    path('search_cafe/name/', views.SearchCafeView.as_view()),
    path('owner_cafes_list/', views.OwnerCafesListView.as_view()),
]
