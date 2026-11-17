"""Корневая маршрутизация Django-проекта."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Администрирование дневника"
admin.site.site_title = "Дневник"
admin.site.index_title = "Управление данными"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("categories/", include("categories.urls")),
    path("entries/", include("entries.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
    ]

handler404 = "homepage.views.page_not_found"
