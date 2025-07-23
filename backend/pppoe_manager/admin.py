from django.contrib import admin

# Customize the admin site header and title
admin.site.site_header = "PPPoE & Hotspot Manager"
admin.site.site_title = "PPPoE Manager Admin"
admin.site.index_title = "Welcome to your Network Management Dashboard"

# Enable sidebar navigation
admin.site.enable_nav_sidebar = True