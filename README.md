# Restful Booker API Tests

## Запуск тестов

Тесты запускаются через `pytest` из корня проекта.

### Окружения

По умолчанию используется окружение `dev`.  
Чтобы запустить тесты на другом окружении, передай флаг `--env`:

```bash
# Dev (по умолчанию)
pytest

# QA
pytest --env=qa

# Stage
pytest --env=stage
```

### Allure-отчёт

По умолчанию результаты тестов пишутся в папку `allure-results` (настроено в `pyproject.toml`).

Сгенерировать и открыть отчёт:

```bash
allure serve allure-results
```

Сохранить отчёт в папку:

```bash
allure generate allure-results -o allure-report --clean
```

### Флаки-тесты и тайм-ауты

Flaky‑тесты автоматически перезапускаются до 2 раз с задержкой 1 секунда:

- `--reruns=2`
- `--reruns-delay=1`

Каждый тест имеет тайм‑аут 60 секунд:

- `--timeout=60`

Эти опции заданы в `pyproject.toml` в секции `[tool.pytest.ini_options]`.

### Линтинг кода (ruff)

Для проверки качества кода используется linter `ruff`:

```bash
ruff check .
```

Автоматические исправления:

```bash
ruff check . --fix
```