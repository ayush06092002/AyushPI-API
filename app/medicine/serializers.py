"""Serializers for medicine API"""

from rest_framework import serializers

from core.models import (
    Medicine,
    Symptom,
)

class SymptomSerializer(serializers.ModelSerializer):
    """Serializer for symptoms"""

    class Meta:
        model = Symptom
        fields = ['id', 'name']


class MedicineSerializer(serializers.ModelSerializer):
    """Serializer for medicine objects"""

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'ref_text', 'dispensing_size', 'dosage' ,'precautions', 'preferred_use']
        read_only_fields = ['id']

class MedicineDetailSerializer(MedicineSerializer):
    """Serializer for medicine detail view"""

    class Meta(MedicineSerializer.Meta):
        fields = MedicineSerializer.Meta.fields
