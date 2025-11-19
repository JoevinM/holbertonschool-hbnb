from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(
        required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(
        required=True, description='ID of the user'),
    'place_id': fields.String
    (required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    """Resource for creating and listing reviews."""

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new review.

        This endpoint allows users to post a review for a specific place.
        It requires a text, a rating, a valid user ID and a valid place ID.

        Returns:
            list: A JSON object containing the new review's details
                (ID, text, rating, user_id, place_id)
            with a 201 status code upon success.

        Errors:
            400 - If the input data is invalid.
            404 - If the specified user or place does not exist.
        """
        review_data = api.payload

        existing_place = facade.get_place(review_data['place_id'])
        if not existing_place:
            return {'error': 'This place doesn\'t exist'}, 404

        current_user = get_jwt_identity()
        user = facade.get_user(current_user)

        review_data['user'] = user

        if current_user == existing_place.user.id:
            return {"message": "You cannot review your own place."}, 400

        for existing_review in existing_place.reviews:
            if current_user == existing_review.user.id:
                return {
                    "message": "You have already reviewed this place."
                }, 400
        review_data['place'] = existing_place
        review_data.pop('place_id')
        try:
            review = facade.create_review(review_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        Returns:
            list: A JSON list of all reviews, each containing ID, text, rating,
            user_id, and place_id, with a 200 status code.
        """
        reviews = facade.get_all_reviews()
        review_list = [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        } for review in reviews]

        return review_list, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Resource for retrieving, updating, or deleting a specific review."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Retrieve a review by its ID.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            list: A JSON object with the review's details
                (ID, text, rating, user_id, place_id)
            and a 200 status code upon success.

        Errors:
            404 - If the review is not found.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """
        Update an existing review.

        This endpoint allows modifying the text, rating, user, or place
        associated with a given review.

        Args:
            review_id (str): The unique identifier of the review to update.

        Returns:
            list: A success message with a 200 status code upon success.

        Errors:
            400 - If the input data is invalid.
            404 - If the review, user, or place is not found.
        """
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404
        update_data = api.payload

        for key in update_data:
            if key == 'place_id' or key == 'user_id' or key == 'id':
                return {'error': 'You cannot modify and enter ids.'}, 403
        for key in update_data:
            if key == 'place' or key == 'user':
                if update_data[key] != getattr(review, key):
                    return {'error: You cannot modify the objects link to the'
                            'review.'}, 403

        current_user = get_jwt_identity()
        if current_user != review.user.id:
            return {"error": "Unauthorized action."}, 403

        try:
            facade.update_review(review_id, update_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review.

        This endpoint removes a review from the database.

        Args:
            review_id (str): The unique identifier of the review to delete.

        Returns:
            list: A success message with a 200 status code upon success.

        Errors:
            404 - If the review is not found.
        """

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user = get_jwt_identity()
        if current_user != review.user_id:
            return {"error": "Unauthorized action."}, 403

        review = facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Resource for retrieving all reviews associated with a specific place."""

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A JSON list of reviews for the given place,
                each containing ID, text, and rating,
            along with a 200 status code.

        Errors:
            404 - If the place is not found.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        review_list = [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in place.reviews]

        return review_list, 200
