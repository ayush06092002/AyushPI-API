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
        read_only_fields = ['id']

class MedicineSerializer(serializers.ModelSerializer):
    """Serializer for medicine objects"""
    symptoms = SymptomSerializer(many=True, required=False)

    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'ref_text', 'dispensing_size', 'dosage' ,'precautions', 'preferred_use',
            'symptoms',
        ]
        read_only_fields = ['id']

    def _get_or_create_symptom(self, symptoms, medicine):
        """Get or create symptom"""
        auth_user = self.context['request'].user
        for symptom in symptoms:
            symptom_obj, create = Symptom.objects.get_or_create(
                user=auth_user,
                **symptom,
            )
            medicine.symptoms.add(symptom_obj)

    def create(self, validated_data):
        """Create a new medicine"""
        symptoms = validated_data.pop('symptoms', [])
        medicine = Medicine.objects.create(**validated_data)
        self._get_or_create_symptom(symptoms, medicine)

        return medicine

    def update(self, instance, validated_data):
        """Update a medicine"""
        symptoms = validated_data.pop('symptoms', [])
        if symptoms is not None:
            instance.symptoms.clear()
            self._get_or_create_symptom(symptoms, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MedicineDetailSerializer(MedicineSerializer):
    """Serializer for medicine detail view"""

    class Meta(MedicineSerializer.Meta):
        fields = MedicineSerializer.Meta.fields

