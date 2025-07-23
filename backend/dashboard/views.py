from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
import json

from users.models import User
from connections.models import Connection
from plans.models import Plan
# from .models import SystemSettings

@staff_member_required
def dashboard_view(request):
    """Main analytics dashboard"""
    context = {
        'page_title': 'Analytics Dashboard',
        'company_name': 'JAMBO WI-FI',
    }
    return render(request, 'dashboard/analytics.html', context)

@staff_member_required
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics"""
    
    # Calculate date ranges
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start - timedelta(days=30)
    
    # Basic counts
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_plans = Plan.objects.filter(is_active=True).count()
    
    # Active connections right now
    active_connections = Connection.objects.filter(
        session_status='active',
        end_time__isnull=True
    ).count()
    
    # Revenue calculations (mock data for now - you can add real billing later)
    today_sessions = Connection.objects.filter(start_time__gte=today_start).count()
    week_sessions = Connection.objects.filter(start_time__gte=week_start).count()
    
    # Estimate revenue based on sessions and average plan price
    avg_plan_price = Plan.objects.filter(is_active=True).aggregate(
        avg_price=Sum('price')
    )['avg_price'] or 0
    
    estimated_today_revenue = today_sessions * (avg_plan_price / total_plans if total_plans > 0 else 0)
    estimated_week_revenue = week_sessions * (avg_plan_price / total_plans if total_plans > 0 else 0)
    
    # User growth data (last 7 days)
    user_growth = []
    for i in range(7):
        day = today_start - timedelta(days=i)
        day_users = User.objects.filter(created_at__date=day.date()).count()
        user_growth.append({
            'date': day.strftime('%m-%d'),
            'count': day_users
        })
    user_growth.reverse()
    
    # Connection types breakdown
    connection_breakdown = Connection.objects.filter(
        start_time__gte=week_start
    ).values('connection_type').annotate(
        count=Count('id')
    )
    
    # Popular plans
    popular_plans = []
    for plan in Plan.objects.filter(is_active=True)[:5]:
        user_count = User.objects.filter(plan_id=plan.id, is_active=True).count()
        popular_plans.append({
            'name': plan.name,
            'users': user_count,
            'price': float(plan.price)
        })
    
    # Session duration stats (last 24 hours)
    recent_sessions = Connection.objects.filter(
        start_time__gte=today_start,
        session_status__in=['stopped', 'timeout']
    )
    
    avg_session_duration = 0
    if recent_sessions.exists():
        total_duration = sum(s.session_duration for s in recent_sessions)
        avg_session_duration = total_duration / recent_sessions.count() / 60  # Convert to minutes
    
    # Data usage stats (rough estimates)
    total_data_usage = Connection.objects.filter(
        start_time__gte=week_start
    ).aggregate(
        total_in=Sum('bytes_in'),
        total_out=Sum('bytes_out')
    )
    
    total_gb = ((total_data_usage['total_in'] or 0) + (total_data_usage['total_out'] or 0)) / (1024**3)
    
    return JsonResponse({
        'overview': {
            'total_users': total_users,
            'active_users': active_users,
            'active_connections': active_connections,
            'total_plans': total_plans,
            'estimated_today_revenue': round(estimated_today_revenue, 2),
            'estimated_week_revenue': round(estimated_week_revenue, 2),
            'avg_session_duration': round(avg_session_duration, 1),
            'total_data_gb': round(total_gb, 2)
        },
        'charts': {
            'user_growth': user_growth,
            'connection_breakdown': list(connection_breakdown),
            'popular_plans': popular_plans
        }
    })

@staff_member_required  
def live_connections_api(request):
    """API for live connection monitoring"""
    
    active_connections = Connection.objects.filter(
        session_status='active',
        end_time__isnull=True
    ).select_related().order_by('-start_time')[:50]
    
    connections_data = []
    for conn in active_connections:
        user = conn.user
        duration = (timezone.now() - conn.start_time).total_seconds()
        
        connections_data.append({
            'username': conn.username,
            'connection_type': conn.get_connection_type_display(),
            'ip_address': conn.ip_address or 'N/A',
            'duration': duration,
            'duration_display': f"{int(duration//3600)}h {int((duration%3600)//60)}m",
            'data_usage': {
                'in': conn.bytes_in,
                'out': conn.bytes_out,
                'total': conn.bytes_in + conn.bytes_out
            },
            'plan_name': user.plan.name if user and user.plan else 'Unknown'
        })
    
    return JsonResponse({
        'connections': connections_data,
        'total_active': len(connections_data)
    })