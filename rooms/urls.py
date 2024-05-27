from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:room_id>", views.RoomDetail.as_view()),
    path("<int:room_id>/reviews", views.RoomReviews.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
