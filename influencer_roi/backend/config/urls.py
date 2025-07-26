"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from influencers.views import InfluencerViewSet, PostViewSet
from tracking.views import TrackingDataViewSet
from payouts.views import PayoutViewSet
from api.views import bulk_upload, clear_database

# Create router and register viewsets
router = DefaultRouter()
router.register(r'influencers', InfluencerViewSet)
router.register(r'posts', PostViewSet)
router.register(r'tracking', TrackingDataViewSet)
router.register(r'payouts', PayoutViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/upload/', bulk_upload, name='bulk_upload'),
    path('api/clear/', clear_database, name='clear_database'),
]
