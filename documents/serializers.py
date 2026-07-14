from pathlib import Path

from rest_framework import serializers

from .models import Document, DocumentChunk


class DocumentSerializer(serializers.ModelSerializer):
    def validate_file(self, file):
        max_size = 10 * 1024 * 1024

        if file.size > max_size:
            raise serializers.ValidationError("O arquivo nao pode passar de 10 MB.")

        extension = Path(file.name).suffix.lower()
        allowed_extensions = {".pdf", ".txt", ".docx"}

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Formato invalido. Envie apenas arquivos PDF, TXT ou DOCX."
            )

        return file

    class Meta:
        model = Document
        fields = [
            "id",
            "owner",
            "title",
            "file",
            "text_content",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "text_content",
            "status",
            "created_at",
            "updated_at",
        ]


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = [
            "id",
            "document",
            "chunk_index",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "document",
            "chunk_index",
            "content",
            "created_at",
        ]
