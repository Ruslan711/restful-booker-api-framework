import allure
import json


class Helper:

    @staticmethod
    def attach_response(response):
        try:
            data = response.json()
        except Exception:
            data = response.text

        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False)
            if isinstance(data, (dict, list))
            else str(data),
            name="response",
            attachment_type=allure.attachment_type.JSON
        )