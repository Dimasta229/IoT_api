from aiohttp import web
from app.db.models import initialize_database, populate_initial_data
from app.handlers.device import handle_post_device, handle_get_device, handle_put_device, handle_delete_device
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    try:
        initialize_database()
        populate_initial_data()
        logger.info("Database initialized and populated with initial data.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def create_app():
    app = web.Application()
    
    app.router.add_post('/device', handle_post_device)
    app.router.add_get('/device/{id}', handle_get_device)
    app.router.add_put('/device/{id}', handle_put_device)
    app.router.add_delete('/device/{id}', handle_delete_device)

    return app

def main():
    setup_database()
    app = create_app()
    
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    main()
