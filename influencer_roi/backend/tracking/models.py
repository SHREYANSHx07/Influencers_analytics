from django.db import models
from influencers.models import Influencer


class TrackingData(models.Model):
    """
    TrackingData model to store campaign performance and revenue tracking
    """
    source = models.CharField(max_length=100, help_text="Data source (e.g., Google Analytics, Shopify)")
    campaign = models.CharField(max_length=255, help_text="Campaign name or identifier")
    brand = models.CharField(max_length=255, help_text="Brand name", default="")
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='tracking_data',
        help_text="Associated influencer"
    )
    user_id = models.CharField(max_length=255, help_text="User identifier from tracking system")
    product = models.CharField(max_length=255, help_text="Product name or SKU")
    date = models.DateField(help_text="Date of the tracking event")
    orders = models.IntegerField(default=0, help_text="Number of orders")
    revenue = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Revenue generated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tracking_data'
        ordering = ['-date', '-created_at']
        verbose_name = 'Tracking Data'
        verbose_name_plural = 'Tracking Data'
        unique_together = ['user_id', 'date', 'product', 'influencer']
    
    def __str__(self):
        return f"{self.campaign} - {self.influencer.name} - {self.date}"
    
    @property
    def average_order_value(self):
        """Calculate average order value"""
        if self.orders == 0:
            return 0
        return self.revenue / self.orders 