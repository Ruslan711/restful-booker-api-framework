import logging
import time
import uuid
from typing import Any

import allure
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from config.environments import EnvironmentConfig
from services.exceptions import ApiError, ApiTimeoutError, ApiConnectionError


logger = logging.getLogger("api")

DEFAULT_TIMEOUT = 10


class BaseAPI:
    def __init__(self, env_config: EnvironmentConfig) -> None:
        self._env_config = env_config
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()

        retry_config = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 503, 504),
            allowed_methods=frozenset(
                {
                    "GET",
                    "HEAD",
                    "OPTIONS",
                    "PUT",
                    "DELETE",
                }
            ),
        )

        adapter = HTTPAdapter(
            max_retries=retry_config,
            pool_connections=20,
            pool_maxsize=20,
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _attach_request(
        self,
        *,
        method: str,
        url: str,
        request_id: str,
        headers: dict[str, Any],
        body: Any,
    ) -> None:
        lines = [
            f"REQUEST_ID: {request_id}",
            f"METHOD: {method}",
            f"URL: {url}",
            "",
            "HEADERS:",
        ]

        for k, v in headers.items():
            lines.append(f"{k}: {v}")

        if body is not None:
            lines += ["", "BODY:", str(body)]

        allure.attach(
            "\n".join(lines),
            name=f"REQUEST {method} {url}",
            attachment_type=allure.attachment_type.TEXT,
        )

    def _attach_response(self, *, request_id: str, response: Response) -> None:
        lines = [
            f"REQUEST_ID: {request_id}",
            f"STATUS: {response.status_code}",
            "",
            "HEADERS:",
        ]

        for k, v in response.headers.items():
            lines.append(f"{k}: {v}")

        body_text = response.text or ""

        lines += ["", "BODY:", body_text]

        allure.attach(
            "\n".join(lines),
            name=f"RESPONSE {response.status_code}",
            attachment_type=allure.attachment_type.TEXT,
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        base = str(self._env_config.booker_url).rstrip("/")
        url = f"{base}{path}"
        request_id = uuid.uuid4().hex

        headers = kwargs.pop("headers", {}) or {}
        headers = headers.copy()
        headers["X-Request-Id"] = request_id

        timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT)
        data = kwargs.get("json") or kwargs.get("data")

        self._attach_request(
            method=method,
            url=url,
            request_id=request_id,
            headers=headers,
            body=data,
        )

        start = time.perf_counter()

        try:
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=timeout,
                **kwargs,
            )
        except requests.exceptions.Timeout as exc:
            raise ApiTimeoutError(f"Timeout: {method} {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise ApiConnectionError(f"Connection error: {method} {url}") from exc
        except requests.exceptions.RequestException as exc:
            raise ApiError(f"Request error: {method} {url}") from exc

        elapsed_ms = int((time.perf_counter() - start) * 1000)

        logger.info(
            "api_request method=%s url=%s status=%s request_id=%s elapsed_ms=%s",
            method,
            url,
            response.status_code,
            request_id,
            elapsed_ms,
        )

        self._attach_response(request_id=request_id, response=response)

        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self._request("DELETE", path, **kwargs)
