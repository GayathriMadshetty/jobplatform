from django.contrib import admin
from .models import Job, Profile, Application
admin.site.register(Job); admin.site.register(Profile)
@admin.register(Application)
class AppAdmin(admin.ModelAdmin):
    list_display = ("user","job","match_score","status","applied_at"); list_editable = ("status",)
