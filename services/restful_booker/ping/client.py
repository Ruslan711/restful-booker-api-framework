from typing import Any, Tuple

from requests import Response

from config.environments import EnvironmentConfig
from services.base_api import BaseAPI


class PingClient(BaseAPI):
    def __init__(self, env_config: EnvironmentConfig) -> None:
        super().__init__(env_config)

    def ping(self, validate: bool = True) -> Tuple[Response, Any]:
        response = self.get("/ping")

        return response, None
