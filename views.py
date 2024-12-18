from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document, User
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import DocumentSerializer
from rest_framework import viewsets
from .models import Document
from rest_framework.permissions import IsAuthenticated
from .ai_processor import classify_document, summarize_document,post_process_classification
from rest_framework.decorators import api_view
from stable_baselines3 import PPO
from .workflow_env import DocumentWorkflowEnv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
from users.serializers import UserSerializer

# View for fetching all users (only accessible by Admin)
class UserManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check ken el user admin
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized access. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, user_id):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized access. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully.", "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized access. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ppo_document_routing.zip")

try:
    rl_model = PPO.load(MODEL_PATH)
    env = DocumentWorkflowEnv()
    print("RL Model loaded successfully!")
except Exception as e:
    print(f"Error loading RL Model: {e}")
    rl_model = None
    env = None

#tstaamel AI classification + RL pour assigner un document au manager approprié
class OptimizeDocumentRoutingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        description = request.data.get("description", "")
        if not description:
            return Response({"error": "Description is required."}, status=400)

        # Step 1: AI Classification
        predicted_label = classify_document(description)  # Use the AI classification result

        # Step 2: Map Document Type to Approver
        approvers = {
            "Promotion Request": "Manager Finance",
            "Change of Work Schedule Request": "Manager RH"
        }
        assigned_manager = approvers.get(predicted_label, "Unassigned")

        # Response to the user
        return Response({
            "message": "Document routing optimized successfully.",
            "document_type": predicted_label,
            "next_approver": assigned_manager
        }, status=200)

#filtrer les documents pour manager specifique
class ManagerDocumentsView(APIView):
    """
    Fetch all documents filtered by manager type.
    Manager RH -> Change of Work Schedule Request
    Manager Finance -> Promotion Request
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Verifier lezm user is a manager
        if user.type_user == "manager_rh":
            documents = Document.objects.filter(document_type="Change of Work Schedule Request")
        elif user.type_user == "manager_finance":
            documents = Document.objects.filter(document_type="Promotion Request")
        else:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize and return the documents
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    


#creation mtaa document bl ia 
class CreateDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check user permissions
        if user.type_user != 'utilisateur':
            return Response({"error": "Only 'utilisateur' can create a document."}, status=status.HTTP_403_FORBIDDEN)

        # Process the input data
        data = request.data.copy()
        description = data.get("description", "")
        if not description:
            return Response({"error": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: AI classification
        ai_label = classify_document(description)
        print("AI-Generated Label (Before Post-Processing):", ai_label)

        # Step 2: Apply manual post-processing rules
        final_label = post_process_classification(description, ai_label)
        print("Final Document Type (After Post-Processing):", final_label)

        # Step 3: AI summarization
        summarized_text = summarize_document(description)

        # Add AI-processed data to request payload
        data["document_type"] = final_label
        data["summary"] = summarized_text

        # Serialize and save the document
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ken admin, ychouf all documents, ken manager ychouf li teb3inou
class GetDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_superuser:
            documents = Document.objects.all()
        elif user.is_staff:
            documents = Document.objects.filter(user=user)  # admin/manager can see their own documents
        else:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
class ManagerDocumentsView(APIView):
    """
    Fetch all documents assigned to the manager based on their type:
    - Manager RH -> Change of Work Schedule Request
    - Manager Finance -> Promotion Request
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Check if the user is a manager
        if user.type_user == "manager_rh":
            documents = Document.objects.filter(document_type="Change of Work Schedule Request")
        elif user.type_user == "manager_finance":
            documents = Document.objects.filter(document_type="Promotion Request")
        else:
            return Response({"error": "Unauthorized access. You are not a manager."}, status=403)

        # Serialize and return the filtered documents
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=200)
#CRUD DOCUMENTS
#mise a jour d'un document (admin et managers)
class UpdateDocumentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        document_id = request.data.get("document_id")
        new_state = request.data.get("new_state")
        try:
            document = Document.objects.get(id_document=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        #admin et managers kahaw
        if user.is_superuser or (user.is_staff and document.user == user):
            document.status = new_state
            document.save()
            return Response({"message": "Document status updated."}, status=status.HTTP_200_OK)
        return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)
#delete document 
class DeleteDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, document_id):
        user = request.user
        try:
            document = Document.objects.get(id_document=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        #admin w managers khw
        if user.is_superuser or (user.is_staff and document.user == user):
            document.delete()
            return Response({"message": "Document deleted."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

@login_required
def manager_dashboard(request):
    return render(request, 'forms/manager.html')
@login_required
def submit_form_view(request):
    return render(request, 'forms/submit_form.html') 