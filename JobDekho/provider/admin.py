from django.contrib import admin
from .models import *
from seeker.models import ScheduleMeeting

admin.site.register(provider_names)

admin.site.register(ScheduleMeeting)

@admin.register(Provider_Profile_Model)
class Provider_Profile_Model_Admin(admin.ModelAdmin):
    list_display = ('user', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area')


@admin.register(city_data)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'state_name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('city')
    
admin.site.register(JobCategory)

from django.contrib import admin
from .models import PostJob

@admin.register(PostJob)
class PostJobAdmin(admin.ModelAdmin):
    list_display = ['title', 'category','salary_min', 'salary_max', 'experience_years', 'created_at']
    list_filter = ['category','experience_years']
    search_fields = ['title', 'description']
