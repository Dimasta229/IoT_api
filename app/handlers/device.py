from aiohttp import web
from app.db.models import Device, Location, ApiUser

async def handle_post_device(request):
    try:
        data = await request.json()
        # Перевірка наявності обов'язкових полів
        required_fields = ['name', 'type', 'login', 'password', 'location_id', 'api_user_id']
        if not all(field in data for field in required_fields):
            return web.json_response({'error': 'Missing fields'}, status=400)
        
        # Перевірка наявності відповідних записів у базі даних
        location = Location.get_or_none(Location.id == data['location_id'])
        api_user = ApiUser.get_or_none(ApiUser.id == data['api_user_id'])
        if not location or not api_user:
            return web.json_response({'error': 'Invalid location or api_user'}, status=400)

        # Створення нового пристрою
        device = Device.create(
            name=data['name'],
            type=data['type'],
            login=data.get('login'),
            password=data.get('password'),
            location=location,
            api_user=api_user
        )
        return web.json_response({'id': device.id}, status=201)
    except Exception as e:
        print(f"Exception: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)

async def handle_get_device(request):
    device_id = request.match_info.get('id')
    try:
        device = Device.get_or_none(Device.id == device_id)
        if not device:
            return web.json_response({'error': 'Device not found'}, status=404)
        
        device_data = {
            'id': device.id,
            'name': device.name,
            'type': device.type,
            'login': device.login,
            'password': device.password,
            'location_id': device.location.id,
            'api_user_id': device.api_user.id
        }
        return web.json_response(device_data, status=200)
    except Exception as e:
        print(f"Exception: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)

async def handle_put_device(request):
    device_id = request.match_info.get('id')
    try:
        data = await request.json()
        device = Device.get_or_none(Device.id == device_id)
        if not device:
            return web.json_response({'error': 'Device not found'}, status=404)
        
        # Оновлення полів
        if 'name' in data:
            device.name = data['name']
        if 'type' in data:
            device.type = data['type']
        if 'login' in data:
            device.login = data['login']
        if 'password' in data:
            device.password = data['password']
        if 'location_id' in data:
            location = Location.get_or_none(Location.id == data['location_id'])
            if location:
                device.location = location
            else:
                return web.json_response({'error': 'Invalid location'}, status=400)
        if 'api_user_id' in data:
            api_user = ApiUser.get_or_none(ApiUser.id == data['api_user_id'])
            if api_user:
                device.api_user = api_user
            else:
                return web.json_response({'error': 'Invalid api_user'}, status=400)
        
        device.save()
        return web.json_response({'id': device.id}, status=200)
    except Exception as e:
        print(f"Exception: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)

async def handle_delete_device(request):
    device_id = request.match_info.get('id')
    try:
        device = Device.get_or_none(Device.id == device_id)
        if not device:
            return web.json_response({'error': 'Device not found'}, status=404)
        
        device.delete_instance()
        return web.json_response({'message': 'Device deleted'}, status=200)
    except Exception as e:
        print(f"Exception: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)
