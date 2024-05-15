from django.contrib import admin
from .models import House  # 같은 폴더에 있는 모델 파일에서 HOUSE 클래스 가져옴

# Register your models here.


@admin.register(House)  # 아래 어드민 패널을 하우스 모델에 적용한다는 설정
class HouseAdmin(admin.ModelAdmin):
    # pass  # admin 모델을 그대로 가져와 쓴다는 의미
    list_display = ("name", "price_per_night", "address", "pets_allowed")
    list_filter = ("price_per_night", "pets_allowed")
