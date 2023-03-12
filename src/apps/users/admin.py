from django.contrib import admin

from apps.users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    readonly_fields = ("modified", "created")
    search_fields = ("nombre_usuario", "created")
    ordering = ("created",)
    date_hierarchy = "created"

    def __str__(self):
        return self.nombre_usuario

    # list_filter=('',)


admin.site.register(User, UserAdmin)
