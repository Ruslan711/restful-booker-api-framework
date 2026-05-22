def test_sanity(env_config):
    """Проверяем, что конфиг окружения поднимается и урл выглядит валидно."""
    assert env_config.booker_url.startswith("http")