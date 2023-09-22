"""Views for Medicine API"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

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

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredients',
            )
        ]
    )
)

class MedicineViewSet(viewsets.ModelViewSet):
    """View for manage medicine APIs"""
    serializer_class = serializers.MedicineDetailSerializer
    queryset = Medicine.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __params_to_names(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return qs.split(',')

    def get_queryset(self):
        """Retrieve the medicines for the authenticated user"""
        symptoms = self.request.query_params.get('symptoms')
        queryset = self.queryset
        if symptoms:
            symptom_names = self.__params_to_names(symptoms)
            queryset = queryset.filter(symptoms__name__in=symptom_names)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def get_serializer_class(self):
        """Return the serializer class for the request"""
        if self.action == 'list':
            return serializers.MedicineSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new medicine"""
        serializer.save(user=self.request.user)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter only assigned symptoms',
            ),
            OpenApiParameter(
                'symptom_names',
                OpenApiTypes.STR,
                description='Filter symptoms by names (comma-separated)',
            )
        ]
    )
)
class BaseMedicineAttrViewSet(mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Base viewset for medicine attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter query set to authenticated user"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        symptom_names = self.request.query_params.get('symptom_names', '') #to remove
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(medicine__isnull=False)

        if symptom_names: #to remove
            symptom_name_list = symptom_names.split(',')
            queryset = queryset.filter(name__in=symptom_name_list)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

class SymptomViewSet(BaseMedicineAttrViewSet):
    """Manage symptoms in the database"""
    serializer_class = serializers.SymptomSerializer
    queryset = Symptom.objects.all()



