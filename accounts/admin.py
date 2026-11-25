from django.contrib import admin
from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favourite_cuisine', 'created_at')
    search_fields = ('user__username', 'user__email', 'favourite_cuisine')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

