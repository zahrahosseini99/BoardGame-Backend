from django.urls import path
from . import views


urlpatterns = [
    path('create_community/', views.CreateCommunityView.as_view()),
    path('community_info/<int:pk>/', views.CommunityInfoPageView.as_view()),
    path('edit_community/<int:pk>/', views.EditCommunityView.as_view()),
    path('search_community/', views.SearchCommunityView.as_view()),
    path('communities_list/', views.CommunitiesListView.as_view()),
    path('owner_communities_list/', views.OwnerCommunitiesListView.as_view()),
    path('member_communities_list/', views.MemberCommunitiesListView.as_view()),
]
