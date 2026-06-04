from typing import Tuple

from requests import Response

from config.environments import EnvironmentConfig
from services.base_api import BaseAPI
from services.restful_booker.auth.models.auth import AuthRequest, AuthResponse


class AuthClient(BaseAPI):
    def __init__(self, env_config: EnvironmentConfig) -> None:
        super().__init__(env_config)

    def create_token(
        self,
        payload: AuthRequest,
        validate: bool = True,
    ) -> Tuple[Response, AuthResponse | None]:
        response = self.post("/auth", json=payload.model_dump())

        if not validate:
            return response, None

        model = AuthResponse.model_validate_json(response.text)
        return response, model
