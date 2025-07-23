from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal

class User(models.Model):
    """Customer accounts - matching existing database schema"""
    
    CONNECTION_TYPES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'), 
        ('both', 'Both'),
    ]
    
    # Fields matching your existing users table exactly
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    
    # Personal information
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)  # Using CharField to match your schema
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Service configuration - using plan_id to match your database
    plan_id = models.IntegerField(help_text="Foreign key to plans table")
    connection_type = models.CharField(max_length=10, choices=CONNECTION_TYPES, default='hotspot')
    
    # Account status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Billing
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        db_table = 'users'  # Use your existing table
        managed = True
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.full_name or 'No name'})"
    
    @property
    def plan(self):
        """Get the plan object (simulates foreign key)"""
        from plans.models import Plan
        try:
            return Plan.objects.get(id=self.plan_id)
        except Plan.DoesNotExist:
            return None
    
    @property
    def is_expired(self):
        """Check if account has expired"""
        if not self.expires_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def status_display(self):
        """Human-readable status"""
        if not self.is_active:
            return "🔴 Disabled"
        elif self.is_expired:
            return "⏰ Expired"  
        else:
            return "✅ Active"