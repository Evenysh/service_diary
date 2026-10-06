"""View-функции главной страницы и общий HTML-каркас."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3" "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с Bootstrap и навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
<nav class="nav">
<a class="nav-link" href="/">Главная</a>
<a class="nav-link" href="/categories/">Категории</a>
<a class="nav-link" href="/entries/">Записи</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница дневника."""
    content = """
<h1 class="display-4">Сервис ведения дневника</h1>
<p class="lead">Личный дневник с привязкой записи к пользователю,
категории и дате.</p>
<p>Основные разделы:</p>
<a href="/categories/" class="btn btn-primary me-2">Категории</a>
<a href="/entries/" class="btn btn-secondary">Записи</a>
"""
    return HttpResponse(page("Дневник", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Своя страница 404 для адресов без маршрута."""
    content = """
<h1 class="text-danger">404 – страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
