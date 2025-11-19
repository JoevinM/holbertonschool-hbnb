from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    """Resource for creating and listing users."""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        This endpoint creates a new user with the provided information.
        The email must be unique in the system.

        Returns:
            list: A JSON object containing the new user's details
                (ID, first name, last name, email)
                and a 201 status code upon success.

        Errors:
            400 - If the email is already registered or
                if the input data is invalid.
        """
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {'id': new_user.id,
                'Success': 'User created successfully !'}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve the list of all registered users.

        Returns:
            list: A JSON list of all users, each containing ID, first name,
            last name, and email, along with a 200 status code.
        """
        users = facade.get_all_users()
        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]

        return user_list, 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Resource for retrieving and updating a specific user."""

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a user's details by ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            list: A JSON object containing the user's ID, first name,
            last name, and email, with a 200 status code upon success.

        Errors:
            404 - If the user is not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user's profile.

        This endpoint allows modifying a user's information such as first name,
        or last name.

        Args:
            user_id (str): The unique identifier of the user to update.

        Returns:
            list: A JSON object containing the updated user's details
            and a 200 status code upon success.

        Errors:
            400 - If the input data is invalid.
            404 - If the user is not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        update_data = api.payload
        current_user = get_jwt_identity()
        if current_user != user_id:
            return {
                "error": "Unauthorized action."
            }, 403
        for key in update_data:
            if key == 'email' or key == 'password' or key == 'id':
                if update_data[key] != getattr(user, key):
                    return {
                        'error': 'You cannot modify email or password.'
                    }, 400

        try:
            facade.update_user(user_id, update_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    """ADMIN ROUTES"""


@api.route('/admin/')
class AdminUserCreate(Resource):
    """Resource for creating and listing users."""
    @jwt_required()
    def post(self):
        """
        Register a new user, only admin can access this route

        This endpoint creates a new user with the provided information.
        The email must be unique in the system.

        Returns:
            list: A JSON object containing the new user's details
                (ID, first name, last name, email)
                and a 201 status code upon success.

        Errors:
            400 - If the email is already registered or
                if the input data is invalid.
            403 - If the user is not an admin
        """

        additionnal_claim = get_jwt()
        if not additionnal_claim["is_admin"]:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = getattr(user_data, 'email', None)

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {'id': new_user.id,
                'Success': 'User created successfully !'}, 201


@api.route('/admin/<user_id>')
class AdminUserResource(Resource):
    """Resource for updating a specific user."""
    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user's profile only admins can access this route.

        This endpoint allows modifying a user's information such as first name,
        last name, email or password.

        Args:
            user_id (str): The unique identifier of the user to update.

        Returns:
            list: A JSON object containing the updated user's details
            and a 200 status code upon success.

        Errors:
            400 - If the input data is invalid.
            403 - If the user is not an admin
            404 - If the user is not found.
        """

        # If 'is_admin' is part of the identity payload
        additionnal_claim = get_jwt()
        if not additionnal_claim["is_admin"]:
            return {'error': 'Admin privileges required'}, 403

        update_data = request.json
        email = update_data.get('email')
        password = update_data.get('password')
        user = facade.get_user(user_id)

        if user is None:
            return {'error': 'User not found'}, 404

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400
        if password:
            user.hash_password(password)
            update_data.pop('password')
        try:
            facade.update_user(user_id, update_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200
