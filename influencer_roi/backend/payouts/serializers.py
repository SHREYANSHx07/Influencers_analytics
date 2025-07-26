from rest_framework import serializers
from .models import Payout


class PayoutSerializer(serializers.ModelSerializer):
    """Serializer for Payout model"""
    influencer_name = serializers.CharField(source='influencer.name', read_only=True)
    roas = serializers.ReadOnlyField()
    
    class Meta:
        model = Payout
        fields = [
            'id', 'influencer', 'influencer_name', 'basis', 'rate',
            'orders', 'total_payout', 'payout_date', 'roas',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PayoutSummarySerializer(serializers.Serializer):
    """Serializer for payout summary statistics"""
    total_payouts = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_orders = serializers.IntegerField()
    average_roas = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_influencers = serializers.IntegerField()
    date_range = serializers.CharField() 