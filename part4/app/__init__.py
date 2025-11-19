from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()

bcrypt = Bcrypt()

db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application with Flask-RESTX.

    This function initializes the Flask app, sets up the RESTX API,
    and registers all namespaces for version 1 of the HBnB API.

    Returns:
        Flask: The configured Flask application instance.
    """
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-RESTX API with documentation
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    db.init_app(app)

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # Register the authentification namespace
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
