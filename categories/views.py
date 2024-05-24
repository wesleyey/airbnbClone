from django.shortcuts import render
from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
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
            new_category = serializer.save()  # create method return value save
            return Response(CategrySerializer(new_category).data)  # re-serialize!
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        raise NotFound
    if request.method == "GET":
        serializer = CategrySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategrySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategrySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
