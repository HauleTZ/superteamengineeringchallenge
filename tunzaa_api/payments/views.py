from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import PaymentPlan, Product
from .serializers import PaymentPlanSerializer, WeeklyContributionSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PaymentPlanViewSet(viewsets.ModelViewSet):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def contribute(self, request, pk=None):
        try:
            plan = PaymentPlan.objects.get(pk=pk, user=request.user)
        except PaymentPlan.DoesNotExist:
            return Response({'detail': 'Payment plan not found.'}, status=404)

        serializer = WeeklyContributionSerializer(data=request.data, context={'payment_plan': plan})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Contribution added successfully.'})
        return Response(serializer.errors, status=400)

