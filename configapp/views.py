from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payout
from .serializer import PayoutSerializer, PayoutStatusSerializer


class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payout = serializer.save()  # status default pending
        # старт асинхронной обработки
        process_payout_task.delay(str(payout.id))
        return Response(PayoutSerializer(payout).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        # разрешаем частичное обновление — в основном для статуса
        instance = self.get_object()
        serializer = PayoutStatusSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PayoutSerializer(instance).data)
