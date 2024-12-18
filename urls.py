from django.urls import path
from .views import (
    DocumentViewSet,
    CreateDocumentView,
    GetDocumentsView,
    UpdateDocumentStatusView,
    DeleteDocumentView,
    OptimizeDocumentRoutingView,
    ManagerDocumentsView
)
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from .views import ManagerDocumentsView,submit_form_view,UserManagementView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('api/documents/get/', GetDocumentsView.as_view(), name='get-documents'),
    path('api/documents/status/update/', UpdateDocumentStatusView.as_view(), name='update-document-status'),
    path('api/documents/delete/<int:document_id>/', DeleteDocumentView.as_view(), name='delete-document'),
    path('api/documents/create/', CreateDocumentView.as_view(), name='create_document'),
    path('api/documents/optimize-routing/', OptimizeDocumentRoutingView.as_view(), name='optimize-routing'),
    path('api/documents/manager-view/', ManagerDocumentsView.as_view(), name='manager-documents'),
    path('api/documents/manager-documents/', ManagerDocumentsView.as_view(), name='manager-documents'),
    path('manager-dashboard/', TemplateView.as_view(template_name="forms/manager_dashboard.html"), name="manager-dashboard"),
    path('submit-form/', submit_form_view, name='submit_form'),
    path('api/admin/users/', UserManagementView.as_view(), name='user-management'),
    path('api/admin/users/<int:user_id>/', UserManagementView.as_view(), name='user-management-detail'),
    path('admin-dashboard/', TemplateView.as_view(template_name="forms/admin_dashboard.html"), name="admin-dashboard"),
]

urlpatterns += router.urls
