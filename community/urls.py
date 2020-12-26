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
    path('day_communities_list/', views.RandomCommunitiesListView.as_view()),
    path('join_community/<int:pk>/', views.JoinCommunityView.as_view()),
    path('leave_community/<int:pk>/', views.LeaveCommunityView.as_view()),
    path('create_event/', views.CreateEventView.as_view()),
    path('join_event/<int:pk>/', views.JoinEventView.as_view()),
]
