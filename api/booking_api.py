from models.booking import BookingRequest


class BookingAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def _build_headers(self, token: str | None = None) -> dict | None:
        if not token:
            return None
        return {"Cookie": f"token={token}"}

    def create(self, request: BookingRequest):
        return self.api_client.post(
            "/booking",
            json=request.model_dump(),
        )

    def get(self, booking_id: int):
        return self.api_client.get(f"/booking/{booking_id}")

    def get_all(self, **filters):
        return self.api_client.get("/booking", params=filters or None)

    def update(self, booking_id: int, request: BookingRequest, token: str | None = None):
        headers = self._build_headers(token)
        return self.api_client.put(
            f"/booking/{booking_id}",
            json=request.model_dump(),
            headers=headers,
        )

    def patch(self, booking_id: int, request: BookingRequest, token: str | None = None):
        headers = self._build_headers(token)
        return self.api_client.patch(
            f"/booking/{booking_id}",
            json=request.model_dump(),
            headers=headers,
        )

    def delete(self, booking_id: int, token: str | None = None):
        headers = self._build_headers(token)
        return self.api_client.delete(f"/booking/{booking_id}", headers=headers)