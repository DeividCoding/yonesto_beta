from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.store.models import UserClient


class UserClientAdmin(BaseAdmin):
    readonly_fields = BaseAdmin.readonly_fields + ("code",)
    search_fields = ("name", "code")
    ordering = ("name",)
    list_display = ("name", "code")

    class Meta:
        verbose_name = "User client"
        verbose_name_plural = "Users client"


admin.site.register(UserClient, UserClientAdmin)
