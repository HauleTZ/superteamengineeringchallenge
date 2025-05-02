from django.urls import path
from .views import PaymentPlanViewSet, ProductViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name='payments'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'payment-plans', PaymentPlanViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

