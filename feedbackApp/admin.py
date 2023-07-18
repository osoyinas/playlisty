from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('score', 'description', 'date')

admin.site.register(Feedback, FeedbackAdmin)