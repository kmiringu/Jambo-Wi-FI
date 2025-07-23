from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("""
    <html>
    <body style="font-family: Arial; padding: 40px; background: #0f172a; color: white;">
        <h1>🚀 PPPoE Manager is Running!</h1>
        <p>Django is working correctly.</p>
        <p><a href="/admin/" style="color: #10b981;">Go to Admin Panel</a></p>
        <p><a href="/dashboard/" style="color: #f59e0b;">Go to Analytics Dashboard</a></p>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', home_view, name='home'),
]