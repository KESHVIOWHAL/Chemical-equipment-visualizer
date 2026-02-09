from django.contrib import admin
from .models import Equipment, Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['uploaded_at']
    search_fields = ['name']
    readonly_fields = ['uploaded_at']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['equipment_name', 'equipment_type']
