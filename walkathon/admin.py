from django.contrib import admin

# Register your models here.
from .models import Walkathon


class WalkathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'starting_day', 'starting_time', 'created_by')


admin.site.register(Walkathon, WalkathonAdmin)
