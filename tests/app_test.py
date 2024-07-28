import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from app.handlers.device import handle_post_device, handle_get_device, handle_put_device, handle_delete_device
from app.db.models import initialize_database, populate_initial_data, Device, ApiUser, Location


@pytest.fixture
async def client():
    initialize_database()
    populate_initial_data()

    app = web.Application()
    app.router.add_post('/device', handle_post_device)
    app.router.add_get('/device/{id}', handle_get_device)
    app.router.add_put('/device/{id}', handle_put_device)
    app.router.add_delete('/device/{id}', handle_delete_device)

    server = TestServer(app)
    client = TestClient(server)

    yield client

    Device.delete().execute()


@pytest.mark.asyncio
async def test_create_device(client):
    response = await client.post('/device', json={
        'name': 'Test Device',
        'type': 'Sensor',
        'login': 'user1',
        'password': 'pass1',
        'location_id': 1,
        'api_user_id': 1
    })

    assert response.status == 201
    data = await response.json()
    assert 'id' in data


@pytest.mark.asyncio
async def test_get_device(client):
    device = Device.create(
        name='Test Device',
        type='Sensor',
        login='user1',
        password='pass1',
        location_id=1,
        api_user_id=1
    )

    response = await client.get(f'/device/{device.id}')
    assert response.status == 200
    data = await response.json()
    assert data['name'] == 'Test Device'
    assert data['type'] == 'Sensor'


@pytest.mark.asyncio
async def test_update_device(client):
    device = Device.create(
        name='Test Device',
        type='Sensor',
        login='user1',
        password='pass1',
        location_id=1,
        api_user_id=1
    )

    response = await client.put(f'/device/{device.id}', json={
        'name': 'Updated Device',
        'type': 'Actuator',
        'login': 'user2',
        'password': 'pass2',
        'location_id': 1,
        'api_user_id': 1
    })

    assert response.status == 200
    data = await response.json()
    assert data['name'] == 'Updated Device'
    assert data['type'] == 'Actuator'


@pytest.mark.asyncio
async def test_delete_device(client):
    device = Device.create(
        name='Test Device',
        type='Sensor',
        login='user1',
        password='pass1',
        location_id=1,
        api_user_id=1
    )

    response = await client.delete(f'/device/{device.id}')
    assert response.status == 200

    response = await client.get(f'/device/{device.id}')
    assert response.status == 404
