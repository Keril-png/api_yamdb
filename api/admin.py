from django.contrib import admin

from .models import CustomUser


class AdminAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'confirmation_code',
        'pk'
    )
    search_fields = ('email',)
    list_filter = ("email",)
    empty_value_display = '-empty-'


admin.site.register(CustomUser, AdminAdmin)
