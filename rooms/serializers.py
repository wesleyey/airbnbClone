from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):

    rating_average = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # photos = PhotoSerializer(many=True, read_only=True)
    photo_set = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating_average",
            "is_owner",
            "photo_set",
        )

    def get_rating_average(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    # review_set = ReviewSerializer(read_only=True, many=True)

    rating_average = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    # photos = PhotoSerializer(many=True, read_only=True)
    photo_set = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1

    def get_rating_average(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()


"""
    def create(self, validated_data):
        print(validated_data)
        return
"""
