from app import create_app
from app.config import Config

if __name__ == "__main__":
    app = create_app()

    app.run(host=Config.SERVER_HOST,
            port=Config.SERVER_PORT,
            debug=Config.DEBUG)
