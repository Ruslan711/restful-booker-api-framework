import requests


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self.session.get(self.base_url + endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(self.base_url + endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.session.put(self.base_url + endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.session.patch(self.base_url + endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(self.base_url + endpoint, **kwargs)