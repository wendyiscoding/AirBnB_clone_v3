#!/usr/bin/python3
"""
app factory
"""
from api.v1.views import app_views
from flask import Flask
import os
from models import storage


def create_app():
    """Creates and configures the application"""

    # Creates a Flask instance
    app = Flask(__name__)

    # Registers blueprint to our Flask instance
    app.register_blueprint(app_views)

    @app.teardown_appcontext
    def teardown_db(error):
        """teardown for application"""
        storage.close()

    return app


if __name__ == "__main__":
    app = create_app()
    if 'HBNB_API_HOST' not in os.environ:
        os.environ['HBNB_API_HOST'] = '0.0.0.0'
    if 'HBNB_API_PORT' not in os.environ:
        os.environ['HBNB_API_PORT'] = 5000
    app.run(host=os.environ['HBNB_API_HOST'], port=os.environ['HBNB_API_PORT'],
            threaded=True)
