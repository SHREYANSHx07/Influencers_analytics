import csv
import json
from io import StringIO
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from influencers.models import Influencer, Post
from tracking.models import TrackingData
from payouts.models import Payout
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def bulk_upload(request):
    """
    Bulk upload endpoint for CSV/JSON data
    Supports: influencers, posts, tracking, payouts
    """
    model_type = request.data.get('model_type')
    file = request.FILES.get('file')
    
    if not model_type or not file:
        return Response({
            'error': 'model_type and file are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate model type
    valid_models = {
        'influencers': Influencer,
        'posts': Post,
        'tracking': TrackingData,
        'payouts': Payout
    }
    
    if model_type not in valid_models:
        return Response({
            'error': f'Invalid model_type. Must be one of: {list(valid_models.keys())}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    model_class = valid_models[model_type]
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        
        # Parse based on file extension
        if file.name.endswith('.csv'):
            data = parse_csv(content)
        elif file.name.endswith('.json'):
            data = json.loads(content)
        else:
            return Response({
                'error': 'File must be CSV or JSON format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process data
        created_count = 0
        errors = []
        
        with transaction.atomic():
            for i, row in enumerate(data):
                try:
                    if model_type == 'influencers':
                        created_count += create_influencer(row)
                    elif model_type == 'posts':
                        created_count += create_post(row)
                    elif model_type == 'tracking':
                        created_count += create_tracking_data(row)
                    elif model_type == 'payouts':
                        created_count += create_payout(row)
                except Exception as e:
                    errors.append(f"Row {i+1}: {str(e)}")
        
        total_records = len(data)
        existing_count = total_records - created_count
        
        return Response({
            'message': f'Processed {total_records} records: {created_count} created, {existing_count} already existed',
            'created_count': created_count,
            'existing_count': existing_count,
            'total_records': total_records,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Upload failed: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


def parse_csv(content):
    """Parse CSV content into list of dictionaries"""
    csv_file = StringIO(content)
    reader = csv.DictReader(csv_file)
    data = list(reader)
    
    # Clean up data by stripping whitespace from all values
    for row in data:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()
    
    return data


def create_influencer(data):
    """Create influencer from data"""
    influencer, created = Influencer.objects.get_or_create(
        name=data['name'],
        defaults={
            'category': data.get('category', ''),
            'gender': data.get('gender', 'other'),
            'follower_count': int(data.get('follower_count', 0)),
            'platform': data.get('platform', 'instagram')
        }
    )
    return 1 if created else 0


def create_post(data):
    """Create post from data"""
    try:
        influencer = Influencer.objects.get(name=data['influencer_name'])
    except Influencer.DoesNotExist:
        raise Exception(f"Influencer '{data['influencer_name']}' not found")
    
    # Validate and clean date format
    post_date = data['date'].strip()
    if not post_date:
        raise Exception("Post date is required")
    
    # Try to parse the date to ensure it's valid
    from datetime import datetime
    try:
        datetime.strptime(post_date, '%Y-%m-%d')
    except ValueError:
        raise Exception(f"Invalid date format: '{post_date}'. Must be YYYY-MM-DD")
    
    post, created = Post.objects.get_or_create(
        influencer=influencer,
        date=post_date,
        platform=data.get('platform', 'instagram'),
        defaults={
            'url': data.get('url', ''),
            'caption': data.get('caption', ''),
            'reach': int(data.get('reach', 0)),
            'likes': int(data.get('likes', 0)),
            'comments': int(data.get('comments', 0))
        }
    )
    return 1 if created else 0


def create_tracking_data(data):
    """Create tracking data from data"""
    try:
        influencer = Influencer.objects.get(name=data['influencer_name'])
    except Influencer.DoesNotExist:
        raise Exception(f"Influencer '{data['influencer_name']}' not found")
    
    # Validate and clean date format
    tracking_date = data['date'].strip()
    if not tracking_date:
        raise Exception("Tracking date is required")
    
    # Try to parse the date to ensure it's valid
    from datetime import datetime
    try:
        datetime.strptime(tracking_date, '%Y-%m-%d')
    except ValueError:
        raise Exception(f"Invalid date format: '{tracking_date}'. Must be YYYY-MM-DD")
    
    tracking_data, created = TrackingData.objects.get_or_create(
        user_id=data['user_id'],
        date=tracking_date,
        product=data['product'],
        influencer=influencer,
        defaults={
            'source': data.get('source', ''),
            'campaign': data.get('campaign', ''),
            'brand': data.get('brand', ''),
            'orders': int(data.get('orders', 0)),
            'revenue': float(data.get('revenue', 0))
        }
    )
    return 1 if created else 0


def create_payout(data):
    """Create payout from data"""
    try:
        influencer = Influencer.objects.get(name=data['influencer_name'])
    except Influencer.DoesNotExist:
        raise Exception(f"Influencer '{data['influencer_name']}' not found")
    
    # Validate and clean date format
    payout_date = data['payout_date'].strip()
    if not payout_date:
        raise Exception("Payout date is required")
    
    # Try to parse the date to ensure it's valid
    from datetime import datetime
    try:
        datetime.strptime(payout_date, '%Y-%m-%d')
    except ValueError:
        raise Exception(f"Invalid date format: '{payout_date}'. Must be YYYY-MM-DD")
    
    payout, created = Payout.objects.get_or_create(
        influencer=influencer,
        payout_date=payout_date,
        basis=data.get('basis', 'post'),
        defaults={
            'rate': float(data.get('rate', 0)),
            'orders': int(data.get('orders', 0)),
            'total_payout': float(data.get('total_payout', 0))
        }
    )
    return 1 if created else 0


@api_view(['POST'])
def clear_database(request):
    """Clear all data from database (for testing purposes)"""
    try:
        with transaction.atomic():
            Payout.objects.all().delete()
            TrackingData.objects.all().delete()
            Post.objects.all().delete()
            Influencer.objects.all().delete()
        
        return Response({
            'message': 'Database cleared successfully',
            'deleted_counts': {
                'payouts': 0,
                'tracking_data': 0,
                'posts': 0,
                'influencers': 0
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': f'Failed to clear database: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 