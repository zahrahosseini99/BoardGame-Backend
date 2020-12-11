from django.urls import path
from . import views

urlpatterns = [
    path('cafe_info/<int:pk>/', views.CafeInfoPageView.as_view()),
    path('create_cafe/', views.CreateCafeView.as_view()),
    path('search_cafe/name/', views.SearchCafeView.as_view()),
    path('owner_cafes_list/', views.OwnerCafesListView.as_view()),
    path('edit_cafe/<int:pk>/', views.EditCafeView.as_view()),
    path('cafe_list/', views.CafeListView.as_view()),
    path('day_cafe_list/', views.RandomCafeListView.as_view()),
]
