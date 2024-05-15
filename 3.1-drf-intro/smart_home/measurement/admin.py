from django.contrib import admin
from .models import Sensor, Measurement


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'sensor_description', 'temperature', 'date']

    @admin.display(ordering='sensor__description')
    def sensor_description(self, obj):
        return obj.sensor.description
