from requests import Response

from services.base_api import BaseAPI

class PingClient(BaseAPI):

    def ping(self, validate: bool = True) -> tuple[Response, None]:
        response = self.get("/ping")
        return response, None
