import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    # Register user
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123"
        }
    )
    assert response.status_code == 201

    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
