from django.db import models
from users.models import User  # Import User model from the users app

class Document(models.Model):
    TYPE_CHOICES = [
        ('Promotion Request', 'Promotion Request'),
        ('Change of Work Schedule Request', 'Change of Work Schedule Request'),
        ('Report', 'Report'),
        ('Invoice', 'Invoice'),
    ]

    id_document = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    document_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Uncategorized')
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f"{self.document_type} by {self.user.name_user}"




