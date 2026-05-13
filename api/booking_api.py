class BookingAPI:

    def __init__(self, api_client):
        self.api_client = api_client

    def create(self, payload: dict):
        return self.api_client.post("/booking", json=payload)

    def get(self, booking_id: int):
        return self.api_client.get(f"/booking/{booking_id}")

    def get_all(self, **filters):
        return self.api_client.get("/booking", params=filters or None)

    def update(self, booking_id: int, payload: dict):
        return self.api_client.put(f"/booking/{booking_id}", json=payload)

    def patch(self, booking_id: int, payload: dict):
        return self.api_client.patch(f"/booking/{booking_id}", json=payload)

    def delete(self, booking_id: int):
        return self.api_client.delete(f"/booking/{booking_id}")