from django.contrib import admin
from viewer.models import DicomImage


class DicomImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(DicomImage, DicomImageAdmin)