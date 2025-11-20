from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Resource for creating and listing places."""

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new place.

        This endpoint allows clients to register a new place by providing
        its title, description, location (latitude, longitude), price
        and a list of amenities's name.

        Returns:
            list: A JSON response containing the created place's details
            and a 201 status code upon success.
            If the place already exists (same coordinates),
                returns a 400 error.
            If the specified owner does not exist, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """

        place_data = api.payload

        existing_place = facade.get_place_by_localisation(
            place_data['latitude'],
            place_data['longitude'])
        if existing_place is True:
            return {'error': 'This place already exists'}, 400

        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        place_data['user'] = user
        amenities = place_data.get('amenities')

        # Getting each amenity object by their name, to put in the list
        if amenities:
            if type(amenities) is not list:
                raise ValueError('error, amenities should be a list')
            list_amenities = []
            for amenity_name in place_data['amenities']:
                new_amenity = facade.get_amenity_by_name(amenity_name)
                if not new_amenity:
                    return {'error': 'One amenity not found'}, 404
                list_amenities.append(new_amenity)
            place_data['amenities'] = list_amenities

        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError):
            return {'error': 'Invalid input data'}, 400

        return {'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.user.id}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all registered places.

        Returns:
            list: A JSON list of all places, each including their ID, title,
            latitude, and longitude, along with a 200 status code.
        """
        places = facade.get_all_places()
        place_list = [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'price' : place.price
        } for place in places]

        return place_list, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource for retrieving, updating, or modifying a specific place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve detailed information about a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A JSON object containing full details of the place,
            including owner information and amenities,
                along with a 200 status code.
            If the place is not found, returns a 404 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        list_amenities = []
        if len(place.amenities) > 0:
            list_amenities = [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                "id": place.user.id,
                "first_name": place.user.first_name,
                "last_name": place.user.last_name,
                "email": place.user.email
            },
            'amenities': list_amenities
        }, 200

    @api.response(404, 'Place not found')
    @api.response(200, 'Amenity added successfuly')
    @jwt_required()
    def post(self, place_id):
        """
        Add an amenity to a specific place.

        This endpoint allows adding an existing amenity to a place.

        Args:
            place_id (str): The unique identifier of the place.

        Payload:
        "amenity": "{the name of the amenity}

        Returns:
            list: A JSON object confirming the addition of the amenity
            with a 200 status code.
            If the place is not found, returns a 404 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user = get_jwt_identity()
        if current_user != place.user.id:
            return {'error': 'Unauthorized action'}, 403

        data_amenity = api.payload
        list_new_amenities = []
        new_amenities = data_amenity.get("amenities")

        if type(new_amenities) is not list:
            return {"error": "amenities must be a list"}

        for name_amenity in data_amenity['amenities']:
            amenity = facade.get_amenity_by_name(name_amenity)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            place.amenities.append(amenity)
            list_new_amenities.append({'id': amenity.id,
                                       'name': amenity.name})
        # Save the add of the new amenities in the database
        db.session.commit()
        return {
            'amenities successfully added': list_new_amenities}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """
        Update an existing place.

        This endpoint allows modifying details of an existing place,
        such as title, description, location, price, owner, or amenities.

        WARNING: If you want to add new amenities to the existing amenities
        please use the Post Method, The Put Method will overwrite the previous
        amenities.

        Args:
            place_id (str): The unique identifier of the place to update.

        Returns:
            list: A success message with a 200 status code upon success.
            If the place is not found, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user = get_jwt_identity()
        data_place = api.payload
        data_amenities = data_place.get('amenities')

        if current_user != place.user.id:
            return {'error': 'Unauthorized action'}, 403
        for key in data_place:
            if key == 'owner_id' or key == 'id':
                return {
                    'error': 'You cannot modify/enter the owner id or'
                    'the place id.'
                }, 403

        if data_amenities:
            if type(data_amenities) is not list:
                return {'error': 'amenities must be a list'}, 400
            list_amenities = []
            for amenity_name in data_amenities:
                new_amenity = facade.get_amenity_by_name(amenity_name)
                if not new_amenity:
                    return {'error': 'One amenity not found'}, 404
                list_amenities.append(new_amenity)
            data_place['amenities'] = list_amenities

        try:
            facade.update_place(place_id, data_place)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Place updated successfully"}, 200

    """ADMIN ROUTES"""


@api.route('/admin/<place_id>')
class AdminPlaceModify(Resource):
    """Resource for updating, or modifying a specific place."""
    @jwt_required()
    def put(self, place_id):
        """
        Update an existing place.

        This endpoint allows modifying details of an existing place,
        such as title, description, location, price, owner, or amenities if
        you are an admin.

        WARNING: If you want to add new amenities to the existing amenities
        please use the Post Method, The Put Method will overwrite the previous
        amenities.

        Args:
            place_id (str): The unique identifier of the place to update.

        Returns:
            list: A success message with a 200 status code upon success.
            If the user is not en admin, returns a 403 error.
            If the place is not found, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """

        current_user = get_jwt_identity()
        additionnal_claim = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = additionnal_claim["is_admin"]

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'place not found'}, 404
        if not is_admin:
            return {'error': 'Unauthorized action'}, 403

        data_place = api.payload
        for key in data_place:
            if key == 'owner_id' or key == 'id' or key == 'user':
                return {
                    'error': 'You cannot modify/enter the owner or the place'
                    'id.'
                }, 403

        data_amenities = data_place.get(("amenities"))
        if data_amenities:
            list_amenities = []
            for amenity_name in data_amenities:
                new_amenity = facade.get_amenity_by_name(amenity_name)
                if not new_amenity:
                    return {'error': 'One amenity not found'}, 404
                list_amenities.append(new_amenity)
            data_place['amenities'] = list_amenities

        try:
            facade.update_place(place_id, data_place)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Place updated successfully"}, 200
