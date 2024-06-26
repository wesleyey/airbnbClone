from django.db import models
from common.models import CommonModel


# Create your models here.
class Room(CommonModel):
    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire Place"
        PRIVATE_ROOM = "private_room", "Private Room"
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(default=False)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    amenities = models.ManyToManyField("rooms.Amenity")
    category = models.ForeignKey(
        "categories.Category",  # appname.classname
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.review_set.count()
        if count == 0:
            return "No Review"
        else:
            total_rating = 0
            for review in self.review_set.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 1)


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        default="",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
