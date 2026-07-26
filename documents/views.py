from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document, DocumentChunk
from .serializers import DocumentSerializer, DocumentChunkSerializer
from .services import (
    extract_text_from_document,
    split_text_into_chunks,
    extract_emails,
    extract_phones
)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user)

        try:
            document.status = "processing"
            document.save(update_fields=["status"])

            text = extract_text_from_document(document)

            if not text:
                raise ValueError("Nao foi possivel extrair texto do documento.")

            emails = extract_emails(text)
            chunks = split_text_into_chunks(text)
            phones = extract_phones(text)

            for index, chunk in enumerate(chunks):

                DocumentChunk.objects.create(
                    document=document,
                    chunk_index=index,
                    content=chunk,
                )

            document.text_content = text
            document.extracted_emails = {
                "emails": emails,
            }
            document.extracted_phones = {
                "phones": phones,
            }

            document.error_message = ""
            document.status = "ready"
            document.save(
                update_fields=[
                    "text_content",
                    "extracted_emails",
                    "extracted_phones",
                    "status",
                    "error_message",
                    "updated_at",
                ]
            )

        except Exception as error:
            document.chunks.all().delete()
            document.status = "failed"
            document.error_message = str(error)
            document.save(update_fields=["status", "error_message", "updated_at"])

    @action(detail=True, methods=["get"])
    def chunks(self, request, pk=None):
        document = self.get_object()
        chunks = document.chunks.order_by("chunk_index")
        serializer = DocumentChunkSerializer(chunks, many=True)
        return Response(serializer.data)
