import pytest
from sqlalchemy import insert, select

from conftest import client, async_session_maker
from src.auth.models import Role


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)

        # fetch all rows as objects
        roles = result.scalars().all()  # use scalars() to get model instances

        # convert the Role objects to tuples or dictionaries for comparison
        roles_data = [(role.id, role.name, role.permissions) for role in roles]

        assert roles_data == [(1, 'admin', None)], "Роль не добавилась"


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })

    assert response.status_code == 201
