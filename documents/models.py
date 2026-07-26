from django.db import models
from django.conf import settings

class Document(models.Model):
  STATUS_CHOICES = [
    ("uploaded", "Uploaded"),
    ("processing","Processing"),
    ("ready", "Ready"),
    ("failed", "Failed"),
  ]

  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="documents"
  )

  title = models.CharField(max_length=255)
  file = models.FileField(upload_to="documents/")
  text_content = models.TextField(blank=True)
  extracted_emails = models.JSONField(
    default=dict,
    blank=True,
)
  extracted_phones = models.JSONField(
      default=dict,
      blank=True,
  )
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="uploaded"
  )
  error_message = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

class DocumentChunk(models.Model):

  document = models.ForeignKey(
    Document,
    on_delete=models.CASCADE,
    related_name="chunks"
  )
  chunk_index = models.PositiveIntegerField()
  content = models.TextField()
  embedding = models.JSONField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)


