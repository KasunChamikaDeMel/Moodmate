from api import create_app
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    # We run the app using the configuration from config.py
    # The host '0.0.0.0' makes the server accessible on your local network
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
