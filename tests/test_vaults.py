from uuid import uuid4

from httpx import AsyncClient, ASGITransport
import pytest

from app.main import app
from app.routers.vaults import _vaults

@pytest.fixture(autouse=True)
def reset_vaults():
    _vaults.clear()
    yield _vaults
    _vaults.clear()

@pytest.fixture()
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

async def test_create_vault(client):
    res = await client.post("/vaults/", json={"name": "myapp/staging"})
    assert res.status_code == 201
    assert res.json()["name"] == "myapp/staging"

async def test_create_duplicate_vault(client):
    res1 = await client.post("/vaults/", json={"name": "myapp/staging"})
    res2 = await client.post("/vaults/", json={"name": "myapp/staging"})
    assert res1.status_code == 201
    assert res2.status_code == 409

async def test_create_vault_invalid_name(client):
    res = await client.post("/vaults/", json={"name": "myApp123/staging"})
    assert res.status_code == 422
    assert "name" in res.json()["detail"][0]["loc"]

async def test_get_vault(client):
    res = await client.post("/vaults/", json={"name": "myapp/staging"})
    vault_id = res.json()["id"]
    vault_name = res.json()["name"]

    get = await client.get(f"/vaults/{vault_id}")
    assert get.status_code == 200
    assert get.json()["id"] == vault_id
    assert get.json()["name"] == vault_name

async def test_get_missing_vault(client):
    non_vault_id = uuid4()

    get = await client.get(f"/vaults/{non_vault_id}")
    assert get.status_code == 404

async def test_list_vaults(client):
    res1 = await client.post("/vaults/", json={"name": "myapp1/staging"})
    res2 = await client.post("/vaults/", json={"name": "myapp2/staging"})

    vault_names = set([res1.json()["name"], res2.json()["name"]])

    get = await client.get("/vaults/")
    assert get.status_code == 200
    assert set([vault["name"] for vault in get.json()]) == vault_names

async def test_delete_vault(client):
    res = await client.post("/vaults/", json={"name": "myapp/staging"})
    vault_id = res.json()["id"]

    delete = await client.delete(f"/vaults/{vault_id}")
    assert delete.status_code == 204
    assert delete.content == b""

    get = await client.get(f"/vaults/{vault_id}")
    assert get.status_code == 404
