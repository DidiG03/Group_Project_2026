from django.urls import path

from .views import (
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentListView,
    DepartmentUpdateView,
    OrganizationStructureView,
    TeamTypeCreateView,
)

urlpatterns = [
    path("departments/", DepartmentListView.as_view(), name="department_list"),
    path("departments/new/", DepartmentCreateView.as_view(), name="department_create"),
    path("departments/<int:pk>/edit/", DepartmentUpdateView.as_view(), name="department_update"),
    path("departments/<int:pk>/delete/", DepartmentDeleteView.as_view(), name="department_delete"),
    path("team-types/new/", TeamTypeCreateView.as_view(), name="teamtype_create"),
    path("structure/", OrganizationStructureView.as_view(), name="organization_structure"),
]
