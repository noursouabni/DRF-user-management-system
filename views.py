from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
def home(request):
    return render(request, 'users/homepage.html')
#personnalisé khatr hachtna b hajet personalisé kima name_user , type_user (bch nsahlou coté frontend)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
#fonction for isadmin
class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)
# CRUD users
#signup (allowany)
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Hash password
            user.save()
            return Response(
                {"message": "User added successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#login (allowany)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    """ 
    Allows login only if the user exists in the database, password matches, and the user is active.
    """
    def post(self, request):
        name_user = request.data.get('name_user')
        password = request.data.get('password')

        try:
            # Check ken user mawjoud in the database
            user = User.objects.get(name_user=name_user)
            
            # verifie ken user is active
            if not user.is_active:
                return Response({"detail": "User account is not active."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Authenticate the user with  password
            if not user.check_password(password):
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login successful."
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
#uniquement lel admin CRUD sur tout les utilisateurs
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    # GET: Retrieve all users or a single user by ID
    def get(self, request, id_user=None):
        if id_user:
            try:
                user = User.objects.get(id_user=id_user)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: Create a new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User added successfully!", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Update an existing user
    def put(self, request, id_user):
        try:
            user = User.objects.get(id_user=id_user)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: Remove a user
    def delete(self, request, id_user):
        permission_classes = [IsAdminPermission]
        try:
            user = User.objects.get(id_user=id_user)
            user.delete()
            return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

def signup_page(request):
    return render(request, 'signup.html')


#pour les utilisateur connectés, interagir avec leurs profile
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "name_user": request.user.name_user,
            "type_user": request.user.type_user
        })

    def put(self, request):
        print("User making request:", request.user)  # Debugging

        new_username = request.data.get("name_user")
        if not new_username:
            return Response({"detail": "Username field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request.user.name_user = new_username
            request.user.save()
            return Response({"detail": "Username updated successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error:", e)
            return Response({"detail": "An error occurred while updating username."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
        try:
            user = request.user
            user.delete()  # Delete the user
            return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("Error deleting user:", e)
            return Response({"detail": "Failed to delete account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

