"""Test for the symptoms API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Symptom,
    Medicine,
)

from medicine.serializers import SymptomSerializer


SYMPTOMS_URL = reverse('medicine:symptom-list')

def detail_url(symptom_name):
    """Create and return a symptom detail URL"""
    return reverse('medicine:symptom-detail', args=[symptom_name])


def create_user(email = 'user@example.com', password = 'testpass123'):
    """Create and return user"""
    return get_user_model().objects.create_user(email = email, password = password)


class PublicSymptomsAPITests(TestCase):
    """Test unauthorized symptoms API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(SYMPTOMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSymptomsAPITests(TestCase):
    """Test unauthorized symptoms API access"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_symptoms(self):
        """Test retrieving symptoms"""
        Symptom.objects.create(user=self.user, name='Sample symptom')
        Symptom.objects.create(user=self.user, name='Sample symptom 2')

        res = self.client.get(SYMPTOMS_URL)

        symptoms = Symptom.objects.all().order_by('-name')
        serializer = SymptomSerializer(symptoms, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_symptoms_limited_to_user(self):
        """Test retrieving symptoms is limited to authenticated user"""
        user2 = create_user(email = 'user2@example.com')
        Symptom.objects.create(user=user2, name='Sample symptom')
        symptom = Symptom.objects.create(user=self.user, name='Sample symptom 2')

        res = self.client.get(SYMPTOMS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], symptom.name)
        self.assertEqual(res.data[0]['id'], symptom.id)

    def test_update_symptom(self):
        """Test updating a symptom"""
        symptom = Symptom.objects.create(user=self.user, name='Sample symptom')
        payload = {'name': 'Updated symptom'}

        url = detail_url(symptom.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        symptom.refresh_from_db()
        self.assertEqual(symptom.name, payload['name'])

    def test_delete_symptom(self):
        """Test deleting a symptom"""
        symptom = Symptom.objects.create(user=self.user, name='Sample symptom')

        url = detail_url(symptom.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        symptoms = Symptom.objects.filter(user = self.user)
        self.assertFalse(symptoms.exists())

    def test_filter_symptoms_assigned_to_medicine(self):
        """Test listing symptoms that are assigned to medicines"""
        symptom1 = Symptom.objects.create(user=self.user, name='Sample symptom 1')
        symptom2 = Symptom.objects.create(user=self.user, name='Sample symptom 2')
        medicine = Medicine.objects.create(
            name='Sample medicine',
            user=self.user,
            ref_text='AFI',
            dispensing_size='200 ml',
            dosage='12 - 24 ml',
            precautions='NS',
            preferred_use='Both'
        )
        medicine.symptoms.add(symptom1)

        res = self.client.get(SYMPTOMS_URL, {'assigned_only': 1})

        serializer1 = SymptomSerializer(symptom1)
        serializer2 = SymptomSerializer(symptom2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filtered_symptoms_unique(self): # TODO: Test this
        """Test filtered symptoms return unique items"""
        symptom = Symptom.objects.create(user=self.user, name='Sample symptom')
        Symptom.objects.create(user=self.user, name='Sample symptom 2')
        medicine1 = Medicine.objects.create(
            name='Sample medicine 1',
            user=self.user,
            ref_text='AFI',
            dispensing_size='200 ml',
            dosage='12 - 24 ml',
            precautions='NS',
            preferred_use='Both'
        )
        medicine1.symptoms.add(symptom)
        medicine2 = Medicine.objects.create(
            name='Sample medicine 2',
            user=self.user,
            ref_text='AFI',
            dispensing_size='200 ml',
            dosage='12 - 24 ml',
            precautions='NS',
            preferred_use='Both'
        )
        medicine2.symptoms.add(symptom)

        res = self.client.get(SYMPTOMS_URL, {'assigned_only': 1})

        self.assertGreaterEqual(len(res.data), 1)
