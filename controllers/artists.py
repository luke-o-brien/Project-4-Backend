from http import HTTPStatus

from flask import Blueprint, request, g
from marshmallow.exceptions import ValidationError
from models.artist import ArtistModel
# from serialisers.venue_comments import VenueCommentSchema
from serialisers.artist import ArtistSchema
from serialisers.artist_comments import ArtistCommentSchema
from middleware.venue_secure_route import venue_secure_route
from middleware.artist_secure_route import artist_secure_route


artist_schema = ArtistSchema()
artist_comments_schema = ArtistCommentSchema()

router = Blueprint("artists", __name__)

@router.route('/artist-signup', methods=["POST"])
def register():
    try:
        artist_dictionary = request.json
        artist = artist_schema.load(artist_dictionary)
        artist.save()
        return artist_schema.jsonify(artist)
    except ValidationError as e:
        return {"errors": e.messages, "messages": "Something went wrong validation"}
    except Exception as e:
        print (e)
        return { "messages": "Something went wrong" }


@router.route('/artist-login', methods=["POST"])
def login():
    try:
        credentials_dictionary = request.json

        #get user by email (from postgresql)
        artist = ArtistModel.query.filter_by(email=credentials_dictionary["email"]).first()

        if not artist:
            return { "message": "No user found for this email" }

        if not artist.validate_password(credentials_dictionary["password"]):
            return {"message": "You are not authorized"}, HTTPStatus.UNAUTHORIZED

        token = artist.generate_token()

        return { "token": token, "message": "Welcome Back!" }

    except Exception as e:
        print (e)
        return { "messages": "Something went wrong" }

# ! G E T  A L L  A R T I S T S
@router.route("/artists", methods=["GET"])
def get_artists():
    artist = ArtistModel.query.all() # query is an object that lives on model and has methods like .all to interface with SQLAlchemy.
    print(type(artist_schema))
    print(type(artist))
    return artist_schema.jsonify(artist, many=True)


# ! G E T  A R T I S T S  B Y  I D
@router.route("/artists/<int:artist_id>", methods=["GET"])
def get_single_artist(artist_id):

    artist = ArtistModel.query.get(artist_id)

    if not artist:

        return { "message": "Artist not found" }, HTTPStatus.NOT_FOUND

    return artist_schema.jsonify(artist)

# ! U P D A T E  A R T I S T S  B Y  I D
@router.route("/artists/<int:artist_id>", methods=["PUT"])
@artist_secure_route # only registered and logged in users can make request
def update_artist(artist_id):
    artist_dictionary = request.json
    # print(coffee_dictionary)

    artist = ArtistModel.query.get(artist_id)
    print(artist)

    if not artist:
        return { "message": "Coffee not found" }, HTTPStatus.NOT_FOUND

    try:
      # .load serializes
        artist_updated = artist_schema.load(
          artist_dictionary, # All the fields you are changing
          instance=artist,  # Existing coffee id that you are updating
          partial=True # Only updates the fields you are updating, without this you have to fill in the entire fields
        )
    except ValidationError as e:
        return { "errors": e.messages, "message": "Something went wrong"}

    artist.save()

    # coffee = CoffeeModel.query.get(coffees_id)
    # print(coffee)

    return artist_schema.jsonify(artist_updated), HTTPStatus.OK


# !  P O S T  A  C O M M E N T  B Y  I D
@router.route("/artists/<int:artist_id>/comments", methods=["POST"])
@venue_secure_route # only registered and logged in users can make request
def create_comment(artist_id):
    
    comment_dictionary = request.json
    comment_dictionary["artist_id"] = artist_id
    comment_dictionary["venue_id"] = g.current_user.id
    print(comment_dictionary)


    try:
        comment = artist_comments_schema.load(comment_dictionary)
        print(comment)
    except ValidationError as e:
        print(e)
        return { "errors": e.messages, "message": "There is no such artist"}, HTTPStatus.NO_CONTENT

    # comment.venue_id = g.current_user
    # comment.artist_id = artist_id
    comment.save()
    print(type(comment))
    return artist_comments_schema.jsonify(comment), HTTPStatus.CREATED