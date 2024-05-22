from django.shortcuts import render
from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategrySerializer

# Create your views here.


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategrySerializer(
            all_categories, many=True
        )  # many 옵션이 없으면 AttributeError at /categories/ 발생
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategrySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)


@api_view()
def category(request, id):
    category = Category.objects.get(id=id)
    serializer = CategrySerializer(category)
    return Response(serializer.data)
