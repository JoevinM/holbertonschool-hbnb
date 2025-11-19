from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Resource for handling creation and retrieval of amenities."""

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.

        This endpoint allows clients to create a new amenity by providing
        a JSON payload with a `name` field.

        Returns:
            list: A JSON response containing the new amenity's ID and name,
            along with a 201 status code upon success.
            If the amenity already exists or the input is invalid, returns
            an error message with status code 400.
        """
        amenity_data = api.payload

        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'This amenity already exist'}, 400
        new_amenity = facade.create_amenity(amenity_data)

        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.

        This endpoint returns a list of all amenities stored in the system.

        Returns:
            list: A JSON list of amenities, each containing an `id` and `name`,
            along with a 200 status code.
        """
        amenities = facade.get_all_amenities()
        amenity_list = [{
            'id': amenity.id,
            'name': amenity.name,
        } for amenity in amenities]

        return amenity_list, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Resource for retrieving and updating a specific amenity by ID."""
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve an amenity by its ID.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            list: A JSON object containing the amenity's `id` and `name`
            with a 200 status code if found.
            If not found, returns an error message with status code 404.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an existing amenity.

        This endpoint allows updating the name of an existing amenity.

        Args:
            amenity_id (str): The unique identifier of the amenity to update.

        Returns:
            list: A success message with a 200 status code
                if the update is successful.
            If the amenity is not found, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity    not found'}, 404
        update_data = api.payload
        existing_amenity = facade.get_amenity_by_name(update_data['name'])
        if existing_amenity:
            return {'error': 'This amenity already exist'}, 400
        for key in update_data:
            if key == 'id':
                if update_data[key] != getattr(amenity, key):
                    return {
                        'error': 'You cannot modify id.'
                    }, 400
        try:
            facade.update_amenity(amenity_id, update_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Amenity updated successfully"}

    """ADMIN ROUTES"""

    @api.route('/admin/')
    class AdminAmenityCreate(Resource):
        """Resource for handling creation of amenities."""
        @jwt_required()
        def post(self):
            """
        Register a new amenity.

        This endpoint allows clients to create a new amenity by providing
        a JSON payload with a `name` field if you are an admin.

        Returns:
            list: A JSON response containing the new amenity's ID and name,
            along with a 201 status code upon success.
            If the user is not an admin, returns an error message with status
            code 403.
            If the amenity already exists or the input is invalid, returns
            an error message with status code 400.
        """

            additionnal_claim = get_jwt()
            if not additionnal_claim["is_admin"]:
                return {'error': 'Admin privileges required'}, 403

            amenity_data = api.payload
            existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
            if existing_amenity:
                return {'error': 'This amenity already exist'}, 400
            new_amenity = facade.create_amenity(amenity_data)

            return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.route('/admin/<amenity_id>')
    class AdminAmenityModify(Resource):
        """Resource for updating a specific amenity by ID."""
        @jwt_required()
        def put(self, amenity_id):
            """
        Update an existing amenity.

        This endpoint allows updating the name of an existing amenity if you
        are an admin.

        Args:
            amenity_id (str): The unique identifier of the amenity to update.

        Returns:
            list: A success message with a 200 status code
                if the update is successful.
            If the user is not an admin, returns a 403 error.
            If the amenity is not found, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """

            additionnal_claim = get_jwt()
            if not additionnal_claim["is_admin"]:
                return {'error': 'Admin privileges required'}, 403

            amenity = facade.get_amenity(amenity_id)

            if not amenity:
                return {'error': 'Amenity not found'}, 404
            update_data = api.payload
            existing_amenity = facade.get_amenity_by_name(update_data['name'])
            if existing_amenity:
                return {'error': 'This amenity already exist'}, 400
            for key in update_data:
                if key == 'id':
                    if update_data[key] != getattr(amenity, key):
                        return {
                            'error': 'You cannot modify id.'
                        }, 400
            try:
                facade.update_amenity(amenity_id, update_data)
            except ValueError:
                return {'error': 'Invalid input data'}, 400

            return {"message": "Amenity updated successfully"}
