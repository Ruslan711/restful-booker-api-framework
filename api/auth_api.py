class AuthAPI:

    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, username: str, password: str):
        return self.api_client.post("/auth", json={
            "username": username,
            "password": password
        })