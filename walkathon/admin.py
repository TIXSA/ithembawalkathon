from django.contrib import admin

from .models import Walkathon, Walker, Streaming, SystemMessages, Entrant, Users, Teams, InformationScreen


class InformationScreenAdmin(admin.ModelAdmin):
    list_display = ('information', 'security_tips', 'frequently_asked_questions', 'terms_and_conditions')


admin.site.register(InformationScreen, InformationScreenAdmin)


class WalkathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'starting_day', 'starting_time', 'created_by')


admin.site.register(Walkathon, WalkathonAdmin)


class WalkerAdmin(admin.ModelAdmin):
    list_display = ('walker_number', 'user_profile', 'walk_method', 'total_walked_distance', 'team')


admin.site.register(Walker, WalkerAdmin)


class StreamingAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'stream_name', 'stream_started', 'stream_ended')


admin.site.register(Streaming, StreamingAdmin)


class SystemMessagesAdmin(admin.ModelAdmin):
    list_display = ('send_condition', 'time_to_be_sent', 'title', 'message_sent')


admin.site.register(SystemMessages, SystemMessagesAdmin)


class EntrantAdmin(admin.ModelAdmin):
    list_display = ('uid', 'eid', 'team_name', 'walk_distance', 'total_amount',  'preferred_communication', 'manual_paid_amount', 'payfast_paid_amount', )


admin.site.register(Entrant, EntrantAdmin)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'email', 'mobile')


admin.site.register(Users, UsersAdmin)


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('wid', 'uid', 'team_name', 'total_amount')


admin.site.register(Teams, TeamsAdmin)
