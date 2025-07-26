from rest_framework import serializers
from .models import TrackingData


class TrackingDataSerializer(serializers.ModelSerializer):
    """Serializer for TrackingData model"""
    influencer_name = serializers.CharField(source='influencer.name', read_only=True)
    influencer_platform = serializers.CharField(source='influencer.platform', read_only=True)
    influencer_category = serializers.CharField(source='influencer.category', read_only=True)
    influencer_gender = serializers.CharField(source='influencer.gender', read_only=True)
    average_order_value = serializers.ReadOnlyField()
    
    class Meta:
        model = TrackingData
        fields = [
            'id', 'source', 'campaign', 'brand', 'influencer', 'influencer_name',
            'influencer_platform', 'influencer_category', 'influencer_gender',
            'user_id', 'product', 'date', 'orders', 'revenue',
            'average_order_value', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TrackingDataSummarySerializer(serializers.Serializer):
    """Serializer for tracking data summary statistics"""
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_orders = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_campaigns = serializers.IntegerField()
    total_brands = serializers.IntegerField()
    total_influencers = serializers.IntegerField()
    date_range = serializers.CharField() 