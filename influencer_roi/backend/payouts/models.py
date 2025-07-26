from django.db import models
from influencers.models import Influencer


class Payout(models.Model):
    """
    Payout model to store influencer compensation data
    """
    BASIS_CHOICES = [
        ('post', 'Per Post'),
        ('order', 'Per Order'),
        ('revenue', 'Revenue Share'),
        ('flat', 'Flat Rate'),
    ]
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='payouts',
        help_text="Associated influencer"
    )
    basis = models.CharField(
        max_length=20, 
        choices=BASIS_CHOICES,
        help_text="Basis for payout calculation"
    )
    rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Rate per post/order/revenue share percentage"
    )
    orders = models.IntegerField(default=0, help_text="Number of orders for this payout")
    total_payout = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total payout amount"
    )
    payout_date = models.DateField(help_text="Date of payout")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payouts'
        ordering = ['-payout_date', '-created_at']
        verbose_name = 'Payout'
        verbose_name_plural = 'Payouts'
    
    def __str__(self):
        return f"{self.influencer.name} - {self.payout_date} (${self.total_payout})"
    
    @property
    def roas(self):
        """Calculate ROAS (Return on Ad Spend)"""
        # Get total revenue for this influencer around the payout date
        from tracking.models import TrackingData
        tracking_data = TrackingData.objects.filter(
            influencer=self.influencer,
            date__gte=self.payout_date,
            date__lte=self.payout_date
        )
        total_revenue = sum(td.revenue for td in tracking_data)
        
        if self.total_payout == 0:
            return 0
        return total_revenue / self.total_payout 