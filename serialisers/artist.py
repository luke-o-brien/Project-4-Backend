from marshmallow import fields
from app import ma

from models.artist import ArtistModel
from serialisers.venue_comments import VenueCommentSchema
from serialisers.artist_genres import GenreSchema

class ArtistSchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = ArtistModel

        load_instance = True

        exclude = ("password_hash",)
        load_only = ('email', 'password')

    comments = fields.Nested("VenueCommentSchema", many=True)
    genre = fields.Nested("GenreSchema", many=True)
    password = fields.String(required=True)
