# from marshmallow import fields
from app import ma
from models.venue import VenueModel
# from serialisers.venue_comments import VenueCommentSchema
# from serialisers.venue_types import TypeSchema


class NestedVenueInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VenueModel
        load_instance = True

        exclude = (
            "password_hash",
            "username",
            "email",
            "type",
            "location",
            "address",
            "budget",
            "websiteUrl",
            "backgroundCardImage",
            "galleryImage1",
            "galleryImage2",
            "galleryImage3",
            "description",
            "fbUrl",
            "twitterUrl",
            "youTubeUrl",
            "instagramUrl",
            "created_at",
            "updated_at",
        )
        # load_only = ('venueName', 'title', 'role', 'profileImage')   
