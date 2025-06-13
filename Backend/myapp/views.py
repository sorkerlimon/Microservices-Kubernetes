from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, UserDetails
from .serializers import CustomUserSerializer, UserDetailsSerializer

# Create your views here.

def home(request):
    """Landing page view"""
    return render(request, 'index.html')


# ----- User endpoints -----

@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = CustomUserSerializer(user, data=request.data, partial=(request.method=="PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----- UserDetails endpoints -----

@api_view(["GET", "POST"])
def userdetails_list(request):
    if request.method == "GET":
        details = UserDetails.objects.all()
        serializer = UserDetailsSerializer(details, many=True)
        return Response(serializer.data)

    serializer = UserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def userdetails_detail(request, pk):
    detail = get_object_or_404(UserDetails, pk=pk)

    if request.method == "GET":
        serializer = UserDetailsSerializer(detail)
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = UserDetailsSerializer(detail, data=request.data, partial=(request.method=="PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
