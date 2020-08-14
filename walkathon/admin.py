from django.contrib import admin

# Register your models here.
from .models import Walkathon, Walker, Streaming, UserMessages


class WalkathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'starting_day', 'starting_time', 'created_by')


class WalkerAdmin(admin.ModelAdmin):
    list_display = ('walker_number', 'user_profile', 'walk_method', 'total_walked_distance', 'team')


class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'message_type', 'title', 'message', 'image_url', 'message_opened')


class StreamingAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'year')


admin.site.register(Walkathon, WalkathonAdmin)
admin.site.register(Walker, WalkerAdmin)
admin.site.register(Streaming, StreamingAdmin)
admin.site.register(UserMessages, UserMessagesAdmin)

