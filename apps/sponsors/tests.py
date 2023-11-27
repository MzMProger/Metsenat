from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.sponsors.choices import SponsorType, SponsorPaymentType, SponsorStatus


class SponsorTests(APITransactionTestCase):
    reset_sequences = True
    fixtures = ["users.json", "sponsors.json"]

    def setUp(self) -> None:
        user = User.objects.get(username="admin")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_sponsor_individual(self):
        url = reverse("sponsors-list")
        data = {
            "full_name": "Numonov Jaxongir",
            "type": SponsorType.INDIVIDUAL,
            "phone_number": "+998999873665",
            "payment_amount": 150000000,
            "payment_type": SponsorPaymentType.CASH
        }
        expecting_data = {
            "id": 2,
            "full_name": "Numonov Jaxongir",
            "type": SponsorType.INDIVIDUAL,
            "phone_number": "+998999873665",
            "organization": None,
            "payment_amount": 150000000,
            "payment_type": SponsorPaymentType.CASH
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expecting_data)

    def test_create_sponsor_legal_entity(self):
        url = reverse("sponsors-list")
        data = {
            "full_name": "Numonov Jaxongir",
            "type": SponsorType.LEGAL_ENTITY,
            "phone_number": "+998999873665",
            "organization": "Sample Organization",
            "payment_amount": 150000000,
            "payment_type": SponsorPaymentType.CASH
        }
        expecting_data = {
            "id": 2,
            "full_name": "Numonov Jaxongir",
            "type": SponsorType.LEGAL_ENTITY,
            "phone_number": "+998999873665",
            "organization": "Sample Organization",
            "payment_amount": 150000000,
            "payment_type": SponsorPaymentType.CASH
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expecting_data)

    def test_list_sponsors(self):
        url = reverse("sponsors-list")
        response = self.client.get(url)
        expecting_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    "full_name": "Olimov Jasur",
                    "phone_number": "+99897770707",
                    'payment_amount': 776000,
                    'spent_amount': 0,
                    'created_at': '2023-09-23T13:02:25.088000Z',
                    "status": SponsorStatus.NEW
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expecting_data)

    def test_update_sponsor(self):
        url = reverse("sponsors-detail", kwargs={"pk": 1})
        data = {
            "full_name": "Olimov Jasur",
            "type": SponsorType.LEGAL_ENTITY,
            "organization": "sample organization",
            "phone_number": "+99897770707",
            'payment_amount': 776000,
            "payment_type": SponsorPaymentType.CASH,
            "status": SponsorStatus.CONFIRMED
        }
        expecting_data = {
            "id": 1,
            "full_name": "Olimov Jasur",
            "type": SponsorType.LEGAL_ENTITY,
            "organization": "sample organization",
            "phone_number": "+99897770707",
            'payment_amount': 776000,
            "payment_type": SponsorPaymentType.CASH,
            "status": SponsorStatus.CONFIRMED
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json(), expecting_data, response.json())

    def test_retrieve_sponsor(self):
        url = reverse("sponsors-detail", kwargs={"pk": 1})
        expecting_data = {
            'id': 1,
            "full_name": "Olimov Jasur",
            "phone_number": "+99897770707",
            'type': SponsorType.LEGAL_ENTITY,
            'payment_amount': 776000,
            "organization": "sample organization",
            'status': SponsorStatus.NEW,
            'created_at': '2023-09-23T13:02:25.088000Z',
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expecting_data)

    def test_destroy_sponsor(self):
        url = reverse("sponsors-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
