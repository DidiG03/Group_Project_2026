from django.contrib import admin
from django.urls import include, path, re_path

from core.views import custom_page_not_found

handler404 = "core.views.custom_page_not_found"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('teams/', include('teams.urls')),
    path('organization/', include('organization.urls')),
    path('messages/', include('messaging_app.urls')),
    path('schedule/', include('scheduling.urls')),
    path('reports/', include('reports.urls')),
    path('analytics/', include('analytics.urls')),
    re_path(r"^.*$", custom_page_not_found, name="page_not_found"),
]
