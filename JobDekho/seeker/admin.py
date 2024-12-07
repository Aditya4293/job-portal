from django.contrib import admin
from .models import *
from django.utils.translation import gettext




# Register your models here.
admin.site.register(seeker_names)
admin.site.register(Seeker_Profile_Model)
admin.site.register(Headline)
admin.site.register(Summary)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Certificate)
admin.site.register(Social)
admin.site.register(Resume)

class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'job', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'job__title']
    actions = ['mark_as_reviewed', 'mark_as_accepted', 'mark_as_rejected']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')

    mark_as_reviewed.short_description = gettext("Mark selected applications as reviewed")

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')

    mark_as_accepted.short_description = gettext("Mark selected applications as accepted")

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')

    mark_as_rejected.short_description = gettext("Mark selected applications as rejected")

admin.site.register(ApplyJob, ApplyJobAdmin)

admin.site.register(Newsletter)