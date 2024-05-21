from django.contrib import admin
from .models import Room, Amenity


# Register your models here.
@admin.action(description="Set all prices to ZERO")
def reset_prices(
    model_admin, request, queryset
):  # in this case queryset is room object
    for room in queryset.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "address",
        "price",
        "total_amenities",
        "rating",
        "owner",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
    )
    search_fields = (
        "owner__username",
        "name",
        "price",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
