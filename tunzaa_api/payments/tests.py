from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from payments.models import Product, PaymentPlan

User = get_user_model()


class PaymentFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass1234')

        # Get JWT token
        token_response = self.client.post('/api/v1/token/', {
            'username': 'testuser',
            'password': 'pass1234'
        })

        access_token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.product = Product.objects.create(name='Smartphone', price=20000)


        self.product = Product.objects.create(name='Smartphone', price=20000)

    def test_create_payment_plan(self):
        response = self.client.post('/api/v1/payment-plans/', {
            'product': self.product.id,
            'weekly_contribution': 5000
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['product'], self.product.id)
        self.assertEqual(response.data['weekly_contribution'], 5000)


    def test_weekly_contributions_until_complete(self):
        # Create a plan
        plan_response = self.client.post('/api/v1/payment-plans/', {
            'product': self.product.id,
            'weekly_contribution': 5000
        })
        plan_id = plan_response.data['id']

        # Make 4 weekly contributions
        for _ in range(4):
            contribute_response = self.client.post(f'/api/v1/payment-plans/{plan_id}/contribute/', {
                'amount': 5000
            })
            self.assertEqual(contribute_response.status_code, 200)
            self.assertIn('Contribution added successfully.', contribute_response.data['detail'])

        # Verify the plan is completed
        plan = PaymentPlan.objects.get(id=plan_id)
        self.assertEqual(plan.total_saved, 20000)
        self.assertTrue(plan.is_completed)
