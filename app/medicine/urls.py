"""URL mappings for medicine app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from medicine import views

app_name = 'medicine'

router = DefaultRouter() # DefaultRouter automatically generates the URL for our viewset
router.register('medicines', views.MedicineViewSet) # register the viewset with our router
router.register('symptoms', views.SymptomViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
