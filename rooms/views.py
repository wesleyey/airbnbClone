from django.shortcuts import render

# from django.http import HttpResponse
from .models import Room

from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Room, Amenity
from categories.models import Category
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from reviews.serializers import ReviewSerializer

# Create your views here.

""" render html 
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "this title comes from django",
        },
    )


def see_one_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
"""

# /api/v1/rooms/amenities
# /api/v1/rooms/amenities/1[id]


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
                # valid 하면 save, save 결과를 serialize 하여 그 데이터를 리턴
            )
        else:
            return Response(serializer.erros)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():

                category_id = request.data.get("category")
                if not category_id:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                # print(request.data.get("amenities"))

                try:
                    with transaction.atomic():

                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )

                        amenities = request.data.get("amenities")
                        for amenity_id in amenities:
                            amenity = Amenity.objects.get(pk=amenity_id)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError(f"Amenity id={amenity_id} does not exist")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        room = self.get_object(room_id)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, room_id):
        room = self.get_object(room_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        # to do put method

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                    else:
                        room.amenities.clear()

                    return Response(RoomDetailSerializer(room).data)
            except Exception as e:
                print(e)
                raise ParseError("amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, room_id):
        room = self.get_object(room_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        try:
            page = request.query_params.get("page", 1)  # defaul 1
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(room_id)
        serializer = ReviewSerializer(
            room.review_set.all()[start, end],
            many=True,
        )
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        room = self.get_object(room_id)
        page_size = 3
        start = page_size * (page - 1)
        end = start + page_size
        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True)

        return Response(serializer.data)
        # to do url connection
