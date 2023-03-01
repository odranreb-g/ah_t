# TODO
# Test mostrando errors de request {}

from http import HTTPStatus
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ah_t.database import get_db
from ah_t.main import app
from ah_t.models import CarOwner


@pytest.fixture
def client_with_auth(db) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app, headers={"X-Token": "fake-super-secret-token"})


@pytest.fixture
def client_without_auth(db) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)


class TestCarOwnersAPI:
    @pytest.mark.parametrize(
        "post, path",
        [
            ("post", "/car-owners/"),
            ("get", "/car-owners/"),
            ("get", "/car-owners/id/"),
            ("patch", "/car-owners/id/"),
        ],
    )
    def test_without_auth(self, client_without_auth: TestClient, post: str, path: str) -> None:
        response = getattr(client_without_auth, post)(path)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_car_owner_missing_value(self, client_with_auth: TestClient) -> None:
        response = client_with_auth.post(
            "/car-owners/",
            json={},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = response.json()
        assert "name" in data["detail"][0]["loc"]
        assert "field required" == data["detail"][0]["msg"]
        assert "value_error.missing" == data["detail"][0]["type"]

    def test_create_car_owner(self, client_with_auth: TestClient) -> None:
        response = client_with_auth.post(
            "/car-owners/",
            json={"name": "Bob"},
        )
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data.keys() == {"id", "name", "sale_opportunity", "is_deleted", "created_at", "updated_at"}

    def test_get_retrieve_car_owner_when_id_is_invalid(self, client_with_auth: TestClient) -> None:
        response = client_with_auth.get(f"/car-owners/{uuid4()}/")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_retrieve_car_owner_when_id_is_valid(
        self, client_with_auth: TestClient, car_owner: CarOwner
    ) -> None:
        response = client_with_auth.get(f"/car-owners/{car_owner.id}/")
        assert response.status_code == HTTPStatus.OK

    def test_partial_update_car_owner_when_id_is_invalid(self, client_with_auth: TestClient) -> None:
        response = client_with_auth.patch(f"/car-owners/{uuid4()}/", json={})
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("test_input", [{"name": "Barbie"}, {"sale_opportunity": False}])
    def test_partial_update_car_owner_when_id_is_valid(
        self, client_with_auth: TestClient, car_owner: CarOwner, test_input: dict[str, Any]
    ) -> None:
        response = client_with_auth.patch(f"/car-owners/{car_owner.id}/", json=test_input)
        assert response.status_code == HTTPStatus.OK

        (key,) = test_input.keys()

        assert response.json()[key] == test_input[key]

    def test_get_list(self, client_with_auth: TestClient, db: Session) -> None:
        for index in range(10):
            db.add(CarOwner(name=f"Owner {index}"))

        db.commit()

        response = client_with_auth.get("/car-owners/")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["count"] == 10
        assert "results" in response.json()
        assert response.json()["next"] is None
        assert response.json()["previous"] is None
