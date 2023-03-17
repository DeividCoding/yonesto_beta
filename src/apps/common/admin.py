from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "modified", "created", "is_removed")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_removed=False)
