"""Views for Medicine API"""

from rest_framework import serializers
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Medicine,
    Symptom,
)
from medicine import serializers

class MedicineViewSet(viewsets.ModelViewSet):
    """View for manage medicine APIs"""
    serializer_class = serializers.MedicineDetailSerializer
    queryset = Medicine.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the medicines for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id') # -id for descending order

    def get_serializer_class(self):
        """Return the serializer class for the request"""
        if self.action == 'list':
            return serializers.MedicineSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new medicine"""
        serializer.save(user=self.request.user)


class SymptomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage symptoms in the database"""
    serializer_class = serializers.SymptomSerializer
    queryset = Symptom.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter query set to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
