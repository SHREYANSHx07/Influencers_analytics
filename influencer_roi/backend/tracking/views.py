from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count
from .models import TrackingData
from .serializers import TrackingDataSerializer, TrackingDataSummarySerializer


class TrackingDataViewSet(viewsets.ModelViewSet):
    """ViewSet for TrackingData model"""
    queryset = TrackingData.objects.select_related('influencer').all()
    serializer_class = TrackingDataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'campaign', 'brand', 'influencer', 'product', 'date', 'influencer__gender', 'influencer__platform', 'influencer__category']
    search_fields = ['campaign', 'brand', 'product', 'influencer__name']
    ordering_fields = ['date', 'orders', 'revenue', 'created_at']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for tracking data"""
        queryset = self.get_queryset()
        
        # Apply date filters if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Apply influencer filters if provided
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_platform = request.query_params.get('influencer__platform')
        influencer_category = request.query_params.get('influencer__category')
        brand = request.query_params.get('brand')
        
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            queryset = queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            queryset = queryset.filter(influencer__category=influencer_category)
        if brand:
            queryset = queryset.filter(brand=brand)
        
        summary = {
            'total_revenue': queryset.aggregate(total=Sum('revenue'))['total'] or 0,
            'total_orders': queryset.aggregate(total=Sum('orders'))['total'] or 0,
            'average_order_value': queryset.aggregate(avg=Avg('revenue'))['avg'] or 0,
            'total_campaigns': queryset.values('campaign').distinct().count(),
            'total_brands': queryset.values('brand').distinct().count(),
            'total_influencers': queryset.values('influencer').distinct().count(),
            'date_range': f"{start_date} to {end_date}" if start_date and end_date else "All time"
        }
        
        serializer = TrackingDataSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_campaign(self, request):
        """Get tracking data grouped by campaign"""
        queryset = self.get_queryset()
        
        campaigns = queryset.values('campaign').annotate(
            total_revenue=Sum('revenue'),
            total_orders=Sum('orders'),
            avg_order_value=Avg('revenue')
        ).order_by('-total_revenue')
        
        return Response(campaigns)
    
    @action(detail=False, methods=['get'])
    def by_influencer(self, request):
        """Get tracking data grouped by influencer"""
        queryset = self.get_queryset()
        
        influencers = queryset.values('influencer__name').annotate(
            total_revenue=Sum('revenue'),
            total_orders=Sum('orders'),
            avg_order_value=Avg('revenue')
        ).order_by('-total_revenue')
        
        return Response(influencers)
    
    @action(detail=False, methods=['get'])
    def roas_analysis(self, request):
        """Get ROAS analysis comparing revenue vs payouts"""
        from payouts.models import Payout
        
        # Get total revenue
        total_revenue = self.get_queryset().aggregate(
            total=Sum('revenue')
        )['total'] or 0
        
        # Get total payouts
        total_payouts = Payout.objects.aggregate(
            total=Sum('total_payout')
        )['total'] or 0
        
        roas = total_revenue / total_payouts if total_payouts > 0 else 0
        
        return Response({
            'total_revenue': total_revenue,
            'total_payouts': total_payouts,
            'roas': roas,
            'roas_percentage': roas * 100
        }) 