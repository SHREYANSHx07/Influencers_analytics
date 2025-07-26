from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count, F, Q, DecimalField
from django.db.models.functions import Coalesce
from .models import Payout
from .serializers import PayoutSerializer, PayoutSummarySerializer
from tracking.models import TrackingData


class PayoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Payout model"""
    queryset = Payout.objects.select_related('influencer').all()
    serializer_class = PayoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['basis', 'influencer', 'payout_date', 'influencer__gender', 'influencer__platform', 'influencer__category']
    search_fields = ['influencer__name']
    ordering_fields = ['payout_date', 'total_payout', 'orders', 'created_at']
    ordering = ['-payout_date']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for payouts with ROAS calculation"""
        queryset = self.get_queryset()
        
        # Apply date filters if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        
        # Apply influencer filters if provided
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_platform = request.query_params.get('influencer__platform')
        influencer_category = request.query_params.get('influencer__category')
        
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            queryset = queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            queryset = queryset.filter(influencer__category=influencer_category)
        
        total_payouts = queryset.aggregate(total=Sum('total_payout'))['total'] or 0
        total_orders = queryset.aggregate(total=Sum('orders'))['total'] or 0
        
        # Calculate overall ROAS by joining with tracking data
        
        if start_date and end_date:
            tracking_queryset = TrackingData.objects.filter(date__range=[start_date, end_date])
        else:
            tracking_queryset = TrackingData.objects.all()
        
        # Apply same influencer filters to tracking data
        if influencer_gender:
            tracking_queryset = tracking_queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            tracking_queryset = tracking_queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            tracking_queryset = tracking_queryset.filter(influencer__category=influencer_category)
        
        total_revenue = tracking_queryset.aggregate(
            total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
        )['total']
        
        # Calculate average ROAS
        average_roas = (total_revenue / total_payouts) if total_payouts > 0 else 0
        
        # Calculate additional metrics
        avg_payout_per_order = (total_payouts / total_orders) if total_orders > 0 else 0
        avg_payout_per_influencer = queryset.values('influencer').distinct().count()
        avg_payout_per_influencer = (total_payouts / avg_payout_per_influencer) if avg_payout_per_influencer > 0 else 0
        
        summary = {
            'total_payouts': total_payouts,
            'total_orders': total_orders,
            'average_roas': round(average_roas, 2),
            'total_influencers': queryset.values('influencer').distinct().count(),
            'avg_payout_per_order': round(avg_payout_per_order, 2),
            'avg_payout_per_influencer': round(avg_payout_per_influencer, 2),
            'total_revenue': total_revenue,
            'date_range': f"{start_date} to {end_date}" if start_date and end_date else "All time"
        }
        
        serializer = PayoutSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_basis(self, request):
        """Get payouts grouped by basis type"""
        queryset = self.get_queryset()
        
        # Apply filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_platform = request.query_params.get('influencer__platform')
        influencer_category = request.query_params.get('influencer__category')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            queryset = queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            queryset = queryset.filter(influencer__category=influencer_category)
        
        basis_types = queryset.values('basis').annotate(
            total_payout=Sum('total_payout'),
            total_orders=Sum('orders'),
            avg_rate=Avg('rate'),
            influencer_count=Count('influencer', distinct=True)
        ).order_by('-total_payout')
        
        # Add avg_roas calculation for each basis type
        for basis_type in basis_types:
            basis_name = basis_type['basis']
            total_payout = basis_type['total_payout']
            
            # Get revenue for this basis type
            if start_date and end_date:
                tracking_queryset = TrackingData.objects.filter(date__range=[start_date, end_date])
            else:
                tracking_queryset = TrackingData.objects.all()
            
            # Apply same filters to tracking data
            if influencer_gender:
                tracking_queryset = tracking_queryset.filter(influencer__gender=influencer_gender)
            if influencer_platform:
                tracking_queryset = tracking_queryset.filter(influencer__platform=influencer_platform)
            if influencer_category:
                tracking_queryset = tracking_queryset.filter(influencer__category=influencer_category)
            
            # For now, we'll use overall revenue since we don't have basis-specific revenue
            total_revenue = tracking_queryset.aggregate(
                total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total']
            
            avg_roas = (total_revenue / total_payout) if total_payout > 0 else 0
            basis_type['avg_roas'] = round(avg_roas, 2)
        
        return Response(basis_types)
    
    @action(detail=False, methods=['get'])
    def by_platform(self, request):
        """Get payouts grouped by platform"""
        queryset = self.get_queryset()
        
        # Apply filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_category = request.query_params.get('influencer__category')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_category:
            queryset = queryset.filter(influencer__category=influencer_category)
        
        platform_data = queryset.values('influencer__platform').annotate(
            total_payout=Sum('total_payout'),
            total_orders=Sum('orders'),
            influencer_count=Count('influencer', distinct=True)
        ).order_by('-total_payout')
        
        # Calculate ROAS for each platform
        for platform in platform_data:
            platform_name = platform['influencer__platform']
            total_payout = platform['total_payout']
            
            # Get revenue for this platform
            if start_date and end_date:
                tracking_queryset = TrackingData.objects.filter(
                    date__range=[start_date, end_date],
                    influencer__platform=platform_name
                )
            else:
                tracking_queryset = TrackingData.objects.filter(influencer__platform=platform_name)
            
            # Apply same filters to tracking data
            if influencer_gender:
                tracking_queryset = tracking_queryset.filter(influencer__gender=influencer_gender)
            if influencer_category:
                tracking_queryset = tracking_queryset.filter(influencer__category=influencer_category)
            
            total_revenue = tracking_queryset.aggregate(
                total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total']
            
            avg_roas = (total_revenue / total_payout) if total_payout > 0 else 0
            platform['avg_roas'] = round(avg_roas, 2)
            platform['total_revenue'] = total_revenue
        
        return Response(platform_data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get payouts grouped by category"""
        queryset = self.get_queryset()
        
        # Apply filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_platform = request.query_params.get('influencer__platform')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            queryset = queryset.filter(influencer__platform=influencer_platform)
        
        category_data = queryset.values('influencer__category').annotate(
            total_payout=Sum('total_payout'),
            total_orders=Sum('orders'),
            influencer_count=Count('influencer', distinct=True)
        ).order_by('-total_payout')
        
        # Calculate ROAS for each category
        for category in category_data:
            category_name = category['influencer__category']
            total_payout = category['total_payout']
            
            # Get revenue for this category
            if start_date and end_date:
                tracking_queryset = TrackingData.objects.filter(
                    date__range=[start_date, end_date],
                    influencer__category=category_name
                )
            else:
                tracking_queryset = TrackingData.objects.filter(influencer__category=category_name)
            
            # Apply same filters to tracking data
            if influencer_gender:
                tracking_queryset = tracking_queryset.filter(influencer__gender=influencer_gender)
            if influencer_platform:
                tracking_queryset = tracking_queryset.filter(influencer__platform=influencer_platform)
            
            total_revenue = tracking_queryset.aggregate(
                total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total']
            
            avg_roas = (total_revenue / total_payout) if total_payout > 0 else 0
            category['avg_roas'] = round(avg_roas, 2)
            category['total_revenue'] = total_revenue
        
        return Response(category_data)
    
    @action(detail=False, methods=['get'])
    def efficiency_metrics(self, request):
        """Get payout efficiency metrics"""
        queryset = self.get_queryset()
        
        # Apply filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        influencer_gender = request.query_params.get('influencer__gender')
        influencer_platform = request.query_params.get('influencer__platform')
        influencer_category = request.query_params.get('influencer__category')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        if influencer_gender:
            queryset = queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            queryset = queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            queryset = queryset.filter(influencer__category=influencer_category)
        
        total_payouts = queryset.aggregate(total=Sum('total_payout'))['total'] or 0
        total_orders = queryset.aggregate(total=Sum('orders'))['total'] or 0
        total_influencers = queryset.values('influencer').distinct().count()
        
        # Calculate efficiency metrics
        avg_payout_per_order = (total_payouts / total_orders) if total_orders > 0 else 0
        avg_payout_per_influencer = (total_payouts / total_influencers) if total_influencers > 0 else 0
        payout_efficiency = (total_orders / total_influencers) if total_influencers > 0 else 0
        
        # Get revenue for ROAS calculation
        if start_date and end_date:
            tracking_queryset = TrackingData.objects.filter(date__range=[start_date, end_date])
        else:
            tracking_queryset = TrackingData.objects.all()
        
        # Apply same filters to tracking data
        if influencer_gender:
            tracking_queryset = tracking_queryset.filter(influencer__gender=influencer_gender)
        if influencer_platform:
            tracking_queryset = tracking_queryset.filter(influencer__platform=influencer_platform)
        if influencer_category:
            tracking_queryset = tracking_queryset.filter(influencer__category=influencer_category)
        
        total_revenue = tracking_queryset.aggregate(
            total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
        )['total']
        
        overall_roas = (total_revenue / total_payouts) if total_payouts > 0 else 0
        
        efficiency_metrics = {
            'total_payouts': total_payouts,
            'total_orders': total_orders,
            'total_influencers': total_influencers,
            'avg_payout_per_order': round(avg_payout_per_order, 2),
            'avg_payout_per_influencer': round(avg_payout_per_influencer, 2),
            'payout_efficiency': round(payout_efficiency, 2),
            'overall_roas': round(overall_roas, 2),
            'total_revenue': total_revenue,
            'date_range': f"{start_date} to {end_date}" if start_date and end_date else "All time"
        }
        
        return Response(efficiency_metrics)
    
    @action(detail=False, methods=['get'])
    def by_influencer(self, request):
        """Get payouts grouped by influencer with ROAS calculation"""
        queryset = self.get_queryset()
        
        # Apply date filters if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            queryset = queryset.filter(payout_date__range=[start_date, end_date])
        
        # Calculate ROAS by joining with tracking data
        influencers = []
        for payout_group in queryset.values('influencer__name').annotate(
            total_payout=Sum('total_payout'),
            total_orders=Sum('orders')
        ).order_by('-total_payout'):
            
            influencer_name = payout_group['influencer__name']
            total_payout = payout_group['total_payout']
            
            # Get total revenue for this influencer from tracking data
            if start_date and end_date:
                tracking_queryset = TrackingData.objects.filter(
                    influencer__name=influencer_name,
                    date__range=[start_date, end_date]
                )
            else:
                tracking_queryset = TrackingData.objects.filter(
                    influencer__name=influencer_name
                )
            
            total_revenue = tracking_queryset.aggregate(
                total=Coalesce(Sum('revenue'), 0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total']
            
            # Calculate ROAS
            avg_roas = (total_revenue / total_payout) if total_payout > 0 else 0
            
            influencers.append({
                'influencer__name': influencer_name,
                'total_payout': total_payout,
                'total_orders': payout_group['total_orders'],
                'avg_roas': round(avg_roas, 2)
            })
        
        return Response(influencers)
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top performing influencers by payout amount"""
        queryset = self.get_queryset()
        
        # Get influencers with highest total payouts
        top_influencers = queryset.values('influencer__name').annotate(
            total_payout=Sum('total_payout'),
            total_orders=Sum('orders')
        ).filter(total_payout__gt=0).order_by('-total_payout')[:10]
        
        return Response(top_influencers) 