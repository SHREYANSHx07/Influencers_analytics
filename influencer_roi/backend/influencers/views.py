from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Influencer, Post
from .serializers import InfluencerSerializer, PostSerializer, InfluencerDetailSerializer


class InfluencerViewSet(viewsets.ModelViewSet):
    """ViewSet for Influencer model"""
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'category', 'gender']
    search_fields = ['name', 'category']
    ordering_fields = ['follower_count', 'created_at', 'name']
    ordering = ['-follower_count']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InfluencerDetailSerializer
        return InfluencerSerializer
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top performing influencers by revenue"""
        from tracking.models import TrackingData
        from django.db.models import Sum
        
        # Get influencers with highest revenue
        influencers = Influencer.objects.annotate(
            total_revenue=Sum('tracking_data__revenue')
        ).filter(total_revenue__gt=0).order_by('-total_revenue')[:10]
        
        serializer = self.get_serializer(influencers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_platform(self, request):
        """Get influencers grouped by platform"""
        from django.db.models import Count
        
        platforms = Influencer.objects.values('platform').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response(platforms)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get influencers grouped by category"""
        from django.db.models import Count
        
        categories = Influencer.objects.values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response(categories)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    queryset = Post.objects.select_related('influencer').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'influencer', 'date']
    search_fields = ['caption', 'influencer__name']
    ordering_fields = ['date', 'reach', 'likes', 'comments', 'created_at']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def top_engaging(self, request):
        """Get posts with highest engagement rates"""
        posts = self.get_queryset().order_by('-likes', '-comments')[:20]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """Get posts within a date range"""
        from datetime import datetime, timedelta
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            posts = self.get_queryset().filter(
                date__range=[start_date, end_date]
            )
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        
        return Response({'error': 'start_date and end_date parameters required'}) 