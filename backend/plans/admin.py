from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Beautiful admin interface for internet plans"""
    
    # What to show in the list view
    list_display = [
        'name', 
        'plan_type', 
        'speed_display', 
        'price_display',
        'time_limit_display',
        'is_active',
        'created_at'
    ]
    
    # Filters on the right sidebar
    list_filter = [
        'plan_type',
        'is_active', 
        'created_at',
        ('price'),  # Price range filter
    ]
    
    # Search functionality
    search_fields = ['name', 'description']
    
    # Default ordering
    ordering = ['price', 'name']
    
    # Fields to show when editing
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'description', 'plan_type', 'is_active')
        }),
        ('Speed Settings', {
            'fields': ('download_speed', 'upload_speed'),
            'description': 'Speeds are in Kbps (Kilobits per second)'
        }),
        ('Pricing & Time', {
            'fields': ('price', 'time_limit'),
            'description': 'Leave time_limit empty for unlimited plans'
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at']
    
    # How many items per page
    list_per_page = 25
    
    # Custom display methods
    def speed_display(self, obj):
        """Show speeds in a nice format"""
        return format_html(
            '<span style="color: green;">⬇️ {}Mbps</span> / '
            '<span style="color: blue;">⬆️ {}Mbps</span>',
            obj.download_speed_mbps,
            obj.upload_speed_mbps
        )
    speed_display.short_description = 'Speed'
    speed_display.admin_order_field = 'download_speed'
    
    def price_display(self, obj):
        """Show price with currency symbol"""
        return format_html('<strong>Ksh{}</strong>', obj.price)
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    
    def time_limit_display(self, obj):
        """Show time limit in human readable format"""
        if obj.is_unlimited:
            return format_html('<span style="color: green;">♾️ Unlimited</span>')
        else:
            hours = obj.time_limit // 60
            minutes = obj.time_limit % 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
    time_limit_display.short_description = 'Time Limit'
    
    def is_active_display(self, obj):
        """Show active status with colors"""
        if obj.is_active:
            return format_html('<span style="color: green;">✅ Active</span>')
        else:
            return format_html('<span style="color: red;">❌ Inactive</span>')
    is_active_display.short_description = 'Status'
    is_active_display.boolean = True  # Adds sorting