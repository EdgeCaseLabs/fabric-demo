from django.contrib import admin
from widgets.models import Widget


class WidgetAdmin(admin.ModelAdmin):
    pass



admin.site.register(Widget, WidgetAdmin)
