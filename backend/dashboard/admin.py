from django.contrib import admin
from django.utils.html import format_html
from .models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """System configuration management"""
    
    list_display = [
        'setting_key',
        'setting_value_display', 
        'setting_type',
        'description',
        'updated_at'
    ]
    
    list_filter = ['setting_type', 'updated_at']
    search_fields = ['setting_key', 'description']
    ordering = ['setting_key']
    
    fieldsets = (
        ('Setting Information', {
            'fields': ('setting_key', 'setting_type', 'description'),
        }),
        ('Value', {
            'fields': ('setting_value',),
            'description': 'Enter the setting value based on the type selected above'
        }),
    )
    
    readonly_fields = ['updated_at']
    
    def setting_value_display(self, obj):
        """Display value with type indication"""
        if obj.setting_type == 'boolean':
            if obj.setting_value.lower() == 'true':
                return format_html('<span style="color: green;">✅ True</span>')
            else:
                return format_html('<span style="color: red;">❌ False</span>')
        elif obj.setting_type == 'integer':
            return format_html('<span style="color: blue;">🔢 {}</span>', obj.setting_value)
        elif obj.setting_type == 'json':
            return format_html('<span style="color: purple;">📄 JSON Data</span>')
        else:
            return obj.setting_value
    setting_value_display.short_description = 'Value'