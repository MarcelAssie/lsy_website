from django.contrib import admin
from .models import Violence

@admin.register(Violence)
class ViolenceAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'date', 'time', 'place', 'reason',
        'severity', 'status', 'reported_by'
    )
    list_filter = ('place', 'reason', 'severity', 'status', 'date')
    search_fields = ('student__nom', 'description', 'reported_by', 'perpetrator', 'other_reason', 'other_place')
    date_hierarchy = 'date'
