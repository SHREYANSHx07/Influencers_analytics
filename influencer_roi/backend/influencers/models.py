import uuid
from django.db import models


class Influencer(models.Model):
    """
    Influencer model to store influencer information
    """
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Influencer's full name")
    category = models.CharField(max_length=100, help_text="Influencer category (e.g., Fashion, Tech, Fitness)")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Influencer's gender")
    follower_count = models.IntegerField(default=0, help_text="Number of followers")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, help_text="Primary platform")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'influencers'
        ordering = ['-follower_count']
        verbose_name = 'Influencer'
        verbose_name_plural = 'Influencers'
    
    def __str__(self):
        return f"{self.name} ({self.platform})"
    
    @property
    def engagement_rate(self):
        """Calculate average engagement rate from posts"""
        posts = self.posts.all()
        if not posts:
            return 0
        
        total_engagement = sum(
            (post.likes + post.comments) / post.reach * 100 
            for post in posts if post.reach > 0
        )
        return total_engagement / len(posts) if posts else 0


class Post(models.Model):
    """
    Post model to store influencer post data
    """
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
    ]
    
    influencer = models.ForeignKey(
        Influencer, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text="Associated influencer"
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, help_text="Platform where post was made")
    date = models.DateField(help_text="Date of the post")
    url = models.URLField(max_length=500, blank=True, null=True, help_text="URL to the post")
    caption = models.TextField(blank=True, null=True, help_text="Post caption or description")
    reach = models.IntegerField(default=0, help_text="Number of people who saw the post")
    likes = models.IntegerField(default=0, help_text="Number of likes")
    comments = models.IntegerField(default=0, help_text="Number of comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-date', '-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.influencer.name} - {self.date} ({self.platform})"
    
    @property
    def engagement_rate(self):
        """Calculate engagement rate for this post"""
        if self.reach == 0:
            return 0
        return ((self.likes + self.comments) / self.reach) * 100 