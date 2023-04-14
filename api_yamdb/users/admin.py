from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'role',
    )
    empty_value_display = '-пусто-'
    list_per_page = 25
    list_max_show_all = 100


admin.site.register(User, UserAdmin)
