from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Customer management interface"""
    
    # List view configuration
    list_display = [
        'username',
        'full_name',
        'plan_display',
        'connection_type_display', 
        'balance_display',
        'status_display',
        'created_at',
        'view_connections_link'
    ]
    
    # Filters
    list_filter = [
        'connection_type',
        'is_active',
        'created_at',
        ('balance'),
        'plan_id',  # Filter by plan
    ]
    
    # Search
    search_fields = [
        'username', 
        'full_name', 
        'email', 
        'phone'
    ]
    
    # Ordering
    ordering = ['-created_at']
    
    # Form layout
    fieldsets = (
        ('Login Information', {
            'fields': ('username', 'password_hash'),
            'description': 'Account credentials'
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'address'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Service Configuration', {
            'fields': ('plan_id', 'connection_type'),
            'description': 'Internet service settings'
        }),
        ('Account Status', {
            'fields': ('is_active', 'expires_at', 'last_login'),
        }),
        ('Billing', {
            'fields': ('balance',),
            'description': 'Account balance and payments'
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'last_login']
    
    # Pagination
    list_per_page = 50
    
    # Actions
    actions = ['activate_users', 'deactivate_users', 'reset_balance']
    
    # Custom display methods
    def plan_display(self, obj):
        """Show plan name instead of ID"""
        plan = obj.plan
        if plan:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:plans_plan_change', args=[plan.id]),
                plan.name
            )
        return "No Plan"
    plan_display.short_description = 'Plan'
    
    def connection_type_display(self, obj):
        """Show connection type with icons"""
        icons = {
            'pppoe': '🔗',
            'hotspot': '📶',
            'both': '🔗📶'
        }
        return f"{icons.get(obj.connection_type, '❓')} {obj.get_connection_type_display()}"
    connection_type_display.short_description = 'Connection'
    
    def balance_display(self, obj):
        """Show balance with color coding"""
        if obj.balance <= 0:
            color = 'red'
            icon = '💳'
        elif obj.balance < 10:
            color = 'orange'
            icon = '⚠️'
        else:
            color = 'green'
            icon = '💰'
        
        return format_html(
            '<span style="color: {};">{} ${}</span>',
            color, icon, obj.balance
        )
    balance_display.short_description = 'Balance'
    balance_display.admin_order_field = 'balance'
    
    def status_display(self, obj):
        """Show comprehensive status"""
        return format_html('<span>{}</span>', obj.status_display)
    status_display.short_description = 'Status'
    
    def view_connections_link(self, obj):
        """Link to view user's connections"""
        url = reverse('admin:connections_connection_changelist')
        return format_html(
            '<a href="{}?user_id={}" target="_blank">View Sessions</a>',
            url, obj.id
        )
    view_connections_link.short_description = 'Sessions'
    
    # Custom actions
    def activate_users(self, request, queryset):
        """Bulk activate users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Bulk deactivate users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def reset_balance(self, request, queryset):
        """Reset balance to zero"""
        updated = queryset.update(balance=0)
        self.message_user(request, f'{updated} user balances reset to Ksh0.')
    reset_balance.short_description = "Reset balance to Ksh0"