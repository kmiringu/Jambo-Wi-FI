from django.db import models
from django.utils import timezone

class Connection(models.Model):
    """Network connections - matching sessions table schema"""
    
    CONNECTION_TYPES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'),
    ]
    
    SESSION_STATUS = [
        ('active', 'Active'),
        ('stopped', 'Stopped'), 
        ('timeout', 'Timeout'),
    ]
    
    # Fields matching your existing sessions table exactly
    user_id = models.IntegerField()  # Foreign key as integer
    username = models.CharField(max_length=50)
    
    # Connection details
    connection_type = models.CharField(max_length=10, choices=CONNECTION_TYPES)
    ip_address = models.CharField(max_length=45, blank=True, null=True)  # IPv4/IPv6
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    nas_ip_address = models.CharField(max_length=45, blank=True, null=True)
    
    # Session timing
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    session_duration = models.IntegerField(default=0)  # seconds
    
    # Data usage
    bytes_in = models.BigIntegerField(default=0)
    bytes_out = models.BigIntegerField(default=0)
    
    # Session status  
    session_status = models.CharField(max_length=10, choices=SESSION_STATUS, default='active')
    terminate_cause = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'sessions'  # Use your existing table name
        managed = True
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.username} - {self.connection_type}"
    
    @property
    def user(self):
        """Get user object"""
        from users.models import User
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    @property
    def is_active(self):
        return self.session_status == 'active'