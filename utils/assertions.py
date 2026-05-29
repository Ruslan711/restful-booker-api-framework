import allure
from requests import Response


@allure.step("Проверка статус-кода: ожидаем {expected}")
def assert_status_code(response: Response, expected: int) -> None:
    actual = response.status_code
    assert actual == expected, f"Ожидали статус-код {expected}, но получили {actual}"


@allure.step("Проверка текста ответа: ожидаем '{expected_text}'")
def assert_response_text(response: Response, expected_text: str) -> None:
    actual = response.text
    assert actual == expected_text, f"Ожидали текст ответа '{expected_text}', но получили '{actual}'"