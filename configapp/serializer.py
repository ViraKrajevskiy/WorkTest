from rest_framework import serializers
from .models import Payout

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['id', 'amount', 'currency', 'recipient', 'status', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']

    def validate_currency(self, value):
        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError('Currency must be 3-letter ISO code.')
        return value.upper()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive.')
        return value


class PayoutStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['status']
