from django.contrib import admin

from app.models import Message, Response

admin.site.register(Message)
admin.site.register(Response)