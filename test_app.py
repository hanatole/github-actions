import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@pytest.mark.parametrize(
    "operation, expected_value",
    [
        ({"a": 2, "b": 10, "operator": "+"}, 12),
        ({"a": 4, "b": 7, "operator": "-"}, -3),
        ({"a": 21, "b": 2, "operator": "*"}, 42),
        ({"a": 2, "b": 10, "operator": "/"}, 0.2),
    ],
)
def test_valid_operation_should_success(operation, expected_value):
    response = client.post("/operation", json=operation)
    assert response.status_code == 200
    assert response.json() == {"value": expected_value}


@pytest.mark.parametrize(
    "operation, expected_error",
    [
        ({"a": 2, "b": 10, "operator": "x"}, "Input should be '+', '-', '*' or '/'"),
        ({"a": 2, "b": 10}, "Field required"),
        (
                {"a": 2, "b": 0, "operator": "/"},
                "Value error, Division by zero is not allowed",
        ),
    ],
)
def test_invalid_operation_should_fail(operation, expected_error):
    response = client.post("/operation", json=operation)
    assert response.status_code == 400
    assert response.json() == {"error": expected_error}
