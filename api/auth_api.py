from models.auth import LoginRequest


class AuthAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, request: LoginRequest):
        return self.api_client.post(
            "/auth",
            json=request.model_dump(),
        )