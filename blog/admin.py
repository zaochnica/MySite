import datetime

from django.contrib import admin
from .models import Training
from .utils import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = 'Отправка писем с требованиями активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'format', 'price', 'date_created')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

#
# class FormatAdmin(admin.ModelAdmin):
#     list_display = ('title', 'content')
#     list_display_links = ('title', 'content')
#     search_fields = ('title', 'content')


# admin.site.register(Format, FormatAdmin)
admin.site.register(Training, TrainingAdmin)
