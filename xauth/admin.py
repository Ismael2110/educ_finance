from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import User, Assign

# Enregistrement des modèles personnalisés
admin.site.register(User)
admin.site.register(Assign)

# Configuration de LogEntry dans l'administration
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_flag', 'content_type']
    search_fields = ['user__username', 'object_repr', 'change_message']
    date_hierarchy = 'action_time'

    # Désactiver l'ajout, la modification et la suppression des logs
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
