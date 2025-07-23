from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    """Real-time connection monitoring"""
    
    # List display
    list_display = [
        'username',
        'connection_type_display',
        'ip_address',
        'session_status_display',
        'duration_display',
        'data_usage_display',
        'start_time',
        'user_link'
    ]
    
    # Filters
    list_filter = [
        'connection_type',
        'session_status',
        'start_time',
        ('start_time'),
    ]
    
    # Search
    search_fields = [
        'username',
        'ip_address', 
        'mac_address'
    ]
    
    # Ordering (newest first)
    ordering = ['-start_time']
    
    # Form layout
    fieldsets = (
        ('User Information', {
            'fields': ('user_id', 'username'),
        }),
        ('Connection Details', {
            'fields': ('connection_type', 'ip_address', 'mac_address', 'nas_ip_address'),
        }),
        ('Session Timing', {
            'fields': ('start_time', 'end_time', 'session_duration'),
        }),
        ('Data Usage', {
            'fields': ('bytes_in', 'bytes_out'),
            'description': 'Data usage in bytes'
        }),
        ('Session Status', {
            'fields': ('session_status', 'terminate_cause'),
        }),
    )
    
    # Read-only fields (most should not be edited)
    readonly_fields = ['start_time', 'session_duration']
    
    # Pagination
    list_per_page = 100
    
    # Actions
    actions = ['terminate_sessions']
    
    # Custom display methods
    def connection_type_display(self, obj):
        """Show connection type with icons"""
        icons = {'pppoe': '🔗', 'hotspot': '📶'}
        return f"{icons.get(obj.connection_type, '❓')} {obj.get_connection_type_display()}"
    connection_type_display.short_description = 'Type'
    
    def session_status_display(self, obj):
        """Show status with colors"""
        colors = {
            'active': 'green',
            'stopped': 'gray', 
            'timeout': 'red'
        }
        icons = {
            'active': '🟢',
            'stopped': '⚫',
            'timeout': '🔴'
        }
        
        return format_html(
            '<span style="color: {};">{} {}</span>',
            colors.get(obj.session_status, 'black'),
            icons.get(obj.session_status, '❓'),
            obj.get_session_status_display()
        )
    session_status_display.short_description = 'Status'
    
    def duration_display(self, obj):
        """Show session duration"""
        if obj.is_active:
            duration = (timezone.now() - obj.start_time).total_seconds()
            return format_html('<span style="color: green;">🕐 {} (ongoing)</span>', obj.duration_display)
        else:
            return obj.duration_display
    duration_display.short_description = 'Duration'
    
    def data_usage_display(self, obj):
        """Show data usage"""
        def format_bytes(bytes_val):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024.0
            return f"{bytes_val:.1f} TB"
        
        total = obj.bytes_in + obj.bytes_out
        if total > 0:
            return format_html(
                '📊 {} total<br><small>⬇️ {} ⬆️ {}</small>',
                format_bytes(total),
                format_bytes(obj.bytes_in),
                format_bytes(obj.bytes_out)
            )
        return "No data"
    data_usage_display.short_description = 'Data Usage'
    
    def user_link(self, obj):
        """Link to user admin page"""
        user = obj.user
        if user:
            url = reverse('admin:users_user_change', args=[user.id])
            return format_html('<a href="{}" target="_blank">👤 View User</a>', url)
        return "Unknown User"
    user_link.short_description = 'User'
    
    # Custom actions
    def terminate_sessions(self, request, queryset):
        """Terminate active sessions"""
        active_sessions = queryset.filter(session_status='active')
        count = 0
        for session in active_sessions:
            session.terminate_session("Admin terminated")
            count += 1
        
        self.message_user(request, f'{count} active sessions terminated.')
    terminate_sessions.short_description = "Terminate active sessions"