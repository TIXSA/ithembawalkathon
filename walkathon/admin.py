from django.contrib import admin

# Register your models here.
from .models import Walkathon, Walker


class WalkathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'starting_day', 'starting_time', 'created_by')


class WalkerAdmin(admin.ModelAdmin):
    list_display = ('walker_number', 'user_profile', 'walk_method', 'total_walked_distance', 'team')


admin.site.register(Walkathon, WalkathonAdmin)
admin.site.register(Walker, WalkerAdmin)
