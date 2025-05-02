# serializers.py

from rest_framework import serializers
from .models import PaymentPlan, Product, Payment
import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger('payments')



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class PaymentPlanSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # To reference Product by ID
    total_amount = serializers.ReadOnlyField(source='product.price')  # Reflect product's price as total_amount

    class Meta:
        model = PaymentPlan
        fields = ['id','product', 'total_amount', 'weekly_contribution']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Set the user from the request context
        return super().create(validated_data)


class WeeklyContributionSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)

    def validate(self, data):
        plan = self.context['payment_plan']
        if plan.is_completed:
            raise serializers.ValidationError("This payment plan is already completed.")
        return data

    def save(self, **kwargs):
        plan: PaymentPlan = self.context['payment_plan']
        amount = self.validated_data['amount']

        # Create a new payment record
        payment = Payment.objects.create(plan=plan, amount=amount)
        

        # Recalculate the total after this payment
        total_saved = plan.total_saved

        
        if total_saved >= plan.target_amount:
            
            plan.is_completed = True
            plan.save()
        
            # Simulate a payout
            logger.info(f"✅ [PAYOUT] Simulated payout for user '{plan.user.username}' on plan ID {plan.id} - Product: {plan.product.name}, Amount: {plan.target_amount} TZS")

        return payment
