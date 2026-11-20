# Restful Booker API Tests

## Что тестирует проект

Тесты проверяют работу API сервиса [Restful Booker](https://restful-booker.herokuapp.com):
- Создание токена авторизации
- Создание бронирования
- Получение списка бронирований и одного бронирования по ID
- Обновление бронирования (PUT и PATCH)
- Удаление бронирования
- Проверка валидации данных

## Технологии

- Python 3.11+
- Pytest
- Requests
- Pydantic
- Allure
- Docker
- GitHub Actions

## Установка зависимостей

Для работы проекта нужен Python 3.11 или выше.

```bash
# Клонировать репозиторий
git clone https://github.com/Ruslan711/restful-booker-api-framework.git
cd restful-booker-api-framework

# Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

## Запуск тестов

Тесты запускаются через `pytest` из корня проекта.

### Окружения

По умолчанию используется окружение `dev`.  
Чтобы запустить тесты на другом окружении, передай флаг `--env`:

```bash
# Dev (по умолчанию)
pytest

# Stage
pytest --env=stage

# Только smoke-тесты
pytest -m smoke
```

### Allure-отчёт

По умолчанию результаты тестов пишутся в папку `allure-results` (настроено в `pytest.ini`).

Сгенерировать и открыть отчёт:

```bash
allure serve allure-results
```

Сохранить отчёт в папку:

```bash
allure generate allure-results -o allure-report --clean
```

![Allure Report](allure-report.png)

### Flaky-тесты и тайм-ауты

Flaky‑тесты автоматически перезапускаются до 2 раз с задержкой 1 секунда:

- `--reruns=2`
- `--reruns-delay=1`

Каждый тест имеет тайм‑аут 60 секунд:

- `--timeout=60`

Эти опции заданы в `pytest.ini`, в `addopts`. Там же параллельный запуск: `-n auto`.

### Линтинг кода (ruff)

Для проверки качества кода используется linter `ruff`:

```bash
ruff check .
```

Автоматические исправления:

```bash
ruff check . --fix
```

## Запуск в Docker

Запустить Docker Desktop.

```bash
docker compose up --build
```

Файл `.env` не обязателен. Логин и пароль по умолчанию: `admin` / `password123`.
Свои значения можно передать переменными `BOOKER_USERNAME` и `BOOKER_PASSWORD`.

HTML-отчёт собирается сам и лежит в `allure-report/index.html`.
Его можно открыть в браузере.
Сырые результаты остаются в `allure-results`.

## GitHub Actions

Тесты запускаются автоматически при каждом push и pull request в `main` (файл `.github/workflows/tests.yml`).
Также можно запустить вручную во вкладке Actions.
HTML-отчёт Allure будет во вкладке Artifacts, архив называется `allure-report`.
