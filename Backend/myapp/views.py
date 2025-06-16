from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, UserDetails
from .serializers import CustomUserSerializer, UserDetailsSerializer
from django.contrib.auth import authenticate

# Create your views here.

def home(request):
    """Landing page view"""
    return render(request, 'index.html')


# ===== API endpoints =====

@extend_schema(responses=CustomUserSerializer(many=True))
@api_view(["GET"])
def user_list_api(request):
    """Retrieve list of all users."""
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@extend_schema(request=CustomUserSerializer, responses=CustomUserSerializer)
@api_view(["POST"])
def user_create_api(request):
    """Create a new user. Expected JSON: {"email": "...", "password": "..."}"""
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=UserDetailsSerializer(many=True))
@api_view(["GET"])
def userdetails_list_api(request):
    """Retrieve list of all user details objects."""
    details = UserDetails.objects.all()
    serializer = UserDetailsSerializer(details, many=True)
    return Response(serializer.data)


@extend_schema(request=UserDetailsSerializer, responses=UserDetailsSerializer)
@api_view(["POST"])
def userdetails_create_api(request):
    """Create user details for a given user_id (no duplicate). Expected JSON: {"user": 1, "first_name": ..., ...}"""
    serializer = UserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=None, responses={200: 'Login success', 400: 'Invalid credentials'})
@api_view(["POST"])
def login_api(request):
    """Authenticate user and return success message."""
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'detail': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    # Optionally, log the user in to create session
    from django.contrib.auth import login as django_login
    django_login(request, user)
    return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)


@extend_schema(responses=UserDetailsSerializer)
@api_view(["GET"])
def userdetails_get_api(request, user_id):
    """Retrieve details for specific user id."""
    detail = get_object_or_404(UserDetails, user__id=user_id)
    serializer = UserDetailsSerializer(detail)
    return Response(serializer.data)
