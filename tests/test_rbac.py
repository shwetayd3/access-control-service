import pytest


@pytest.mark.asyncio
async def test_admin_protected_route(client):
    # Create admin user
    await client.post(
        "/auth/register",
        json={
            "email": "admin@test.com",
            "password": "StrongPassword123"
        }
    )

    login = await client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "StrongPassword123"
        }
    )

    token = login.json()["access_token"]

    # Access admin endpoint without role
    response = await client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
