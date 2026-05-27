from typing import Tuple
from requests import Response

from services.base_api import BaseAPI


class PingClient(BaseAPI):

    def ping(self) -> Tuple[Response, None]:
        return self.get("/ping"), None
