from django.db import models
import json

class SystemSettings(models.Model):
    """System settings - matching existing table"""
    
    SETTING_TYPES = [
        ('string', 'String'),
        ('integer', 'Integer'), 
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ]
    
    # Fields matching your existing system_settings table
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    setting_type = models.CharField(max_length=10, choices=SETTING_TYPES, default='string')
    updated_at = models.DateTimeField(auto_now=True)  # This one exists in your table
    
    class Meta:
        db_table = 'system_settings'
        managed = True
    
    def __str__(self):
        return self.setting_key
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get a setting value safely"""
        try:
            setting = cls.objects.get(setting_key=key)
            return setting.get_value()
        except cls.DoesNotExist:
            return default
        except Exception:
            return default