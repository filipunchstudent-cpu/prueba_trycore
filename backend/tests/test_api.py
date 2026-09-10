from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base, get_db
from backend.app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_evm.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_creates_project_with_empty_metrics():
    response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Proyecto demo"
    assert data["activities"] == []
    assert data["metrics"]["bac"] == "0"
    assert data["metrics"]["pv"] == "0"
    assert data["metrics"]["ev"] == "0"
    assert data["metrics"]["cpi"] is None
    assert data["metrics"]["spi"] is None


def test_creates_activity_and_returns_evm_metrics():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    response = client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "Desarrollo",
            "bac": "4000",
            "planned_percent": "50",
            "actual_percent": "25",
            "ac": "1500",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Desarrollo"
    assert str(round(float(data["metrics"]["pv"]))) == "2000"
    assert str(round(float(data["metrics"]["ev"]))) == "1000"
    assert str(round(float(data["metrics"]["cv"]))) == "-500"
    assert str(round(float(data["metrics"]["sv"]))) == "-1000"
    assert round(Decimal(data["metrics"]["cpi"]),4) ==round(Decimal("1000")/Decimal("1500"),4)
    assert data["metrics"]["spi"] == "0.5"


def test_gets_project_with_consolidated_metrics():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "Descubrimiento",
            "bac": "1000",
            "planned_percent": "100",
            "actual_percent": "100",
            "ac": "800",
        },
    )

    client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "Desarrollo",
            "bac": "4000",
            "planned_percent": "50",
            "actual_percent": "25",
            "ac": "1500",
        },
    )

    response = client.get(f"/api/projects/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert str(round(float(data["metrics"]["bac"]))) == "5000"
    assert str(round(float(data["metrics"]["pv"]))) == "3000"
    assert str(round(float(data["metrics"]["ev"]))) == "2000"
    assert str(round(float(data["metrics"]["ac"]))) == "2300"
    assert str(round(float(data["metrics"]["cv"]))) == "-300"
    assert str(round(float(data["metrics"]["sv"]))) == "-1000"


def test_updates_project():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto inicial"},
    )

    project_id = project_response.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Proyecto actualizado"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Proyecto actualizado"


def test_updates_activity():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    activity_response = client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "Desarrollo",
            "bac": "4000",
            "planned_percent": "50",
            "actual_percent": "25",
            "ac": "1500",
        },
    )

    activity_id = activity_response.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}/activities/{activity_id}",
        json={
            "name": "Desarrollo actualizado",
            "bac": "4000",
            "planned_percent": "50",
            "actual_percent": "50",
            "ac": "1500",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Desarrollo actualizado"
    assert str(round(float(response.json()["metrics"]["ev"]))) == "2000"


def test_deletes_activity():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    activity_response = client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "Desarrollo",
            "bac": "4000",
            "planned_percent": "50",
            "actual_percent": "25",
            "ac": "1500",
        },
    )

    activity_id = activity_response.json()["id"]

    response = client.delete(f"/api/projects/{project_id}/activities/{activity_id}")

    assert response.status_code == 204

    project = client.get(f"/api/projects/{project_id}").json()
    assert project["activities"] == []


def test_deletes_project():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    response = client.delete(f"/api/projects/{project_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/projects/{project_id}")
    assert get_response.status_code == 404


def test_returns_404_when_project_does_not_exist():
    response = client.get("/api/projects/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_rejects_invalid_activity_payload():
    project_response = client.post(
        "/api/projects",
        json={"name": "Proyecto demo"},
    )

    project_id = project_response.json()["id"]

    response = client.post(
        f"/api/projects/{project_id}/activities",
        json={
            "name": "",
            "bac": "-1",
            "planned_percent": "120",
            "actual_percent": "25",
            "ac": "1500",
        },
    )

    assert response.status_code == 422