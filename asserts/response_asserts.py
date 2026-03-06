class ResponseAsserts:
    @staticmethod
    def assert_status(response, expected_status):
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

    @staticmethod
    def assert_content_type(response, expected_ct="application/json"):
        ct = response.headers.get("Content-Type", "")
        assert expected_ct in ct, f"Expected Content-Type '{expected_ct}', got '{ct}'"

    @staticmethod
    def assert_json_schema(response, required_keys):
        data = response.json()
        for key in required_keys:
            assert key in data, f"Key '{key}' not found in response JSON"

    @staticmethod
    def assert_error_message(response, expected_message):
        data = response.json()
        assert data.get("detail") == expected_message, \
            f"Expected error message '{expected_message}', got '{data.get('detail')}'"