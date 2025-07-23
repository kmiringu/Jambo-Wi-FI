from django.db import models
from django.core.validators import MinValueValidator

class Plan(models.Model):
    """Internet service plans with bandwidth and pricing"""
    
    # Plan types (matching your database ENUM)
    PLAN_TYPES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'),
        ('both', 'Both PPPoE & Hotspot'),
    ]
    
    # Fields that match your existing database exactly
    name = models.CharField(max_length=100, help_text="Plan name")
    description = models.TextField(blank=True, help_text="Plan description")
    
    # Speed settings (in Kbps) - matching your database
    download_speed = models.PositiveIntegerField(help_text="Download speed in Kbps")
    upload_speed = models.PositiveIntegerField(help_text="Upload speed in Kbps")
    
    # Time and pricing - matching your database
    time_limit = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Time limit in minutes. NULL = unlimited."
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Price in local currency"
    )
    
    # Configuration - matching your database
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, default='hotspot')
    is_active = models.BooleanField(default=True)
    
    # Timestamp - only created_at exists in your database
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'plans'  # Use your existing table
        managed = True      # Django can manage this table
        ordering = ['price', 'name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def download_speed_mbps(self):
        """Convert download speed to Mbps"""
        return round(self.download_speed / 1024, 2)
    
    @property
    def upload_speed_mbps(self):
        """Convert upload speed to Mbps"""  
        return round(self.upload_speed / 1024, 2)
    
    @property
    def is_unlimited(self):
        """Check if plan has unlimited time"""
        return self.time_limit is None