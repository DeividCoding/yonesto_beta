from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "modified", "created", "is_removed")
