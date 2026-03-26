from django.urls import path

from .views import (
    TeamCreateView,
    TeamDeleteView,
    TeamDependencyCreateView,
    TeamDetailView,
    TeamListView,
    TeamMemberCreateView,
    TeamMemberDeleteView,
    TeamUpdateView,
)

urlpatterns = [
    path("", TeamListView.as_view(), name="team_list"),
    path("new/", TeamCreateView.as_view(), name="team_create"),
    path("<int:pk>/edit/", TeamUpdateView.as_view(), name="team_update"),
    path("<int:pk>/delete/", TeamDeleteView.as_view(), name="team_delete"),
    path("members/new/", TeamMemberCreateView.as_view(), name="team_member_create"),
    path("members/<int:pk>/delete/", TeamMemberDeleteView.as_view(), name="team_member_delete"),
    path("dependencies/new/", TeamDependencyCreateView.as_view(), name="team_dependency_create"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
]
