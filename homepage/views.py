"""View-функции главной страницы."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница дневника."""
    return render(request, "homepage/index.html")


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Своя страница 404 для адресов без маршрута."""
    return render(request, "homepage/page_not_found.html", status=404)
