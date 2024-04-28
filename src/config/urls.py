from django.contrib import admin
from django.urls import path
from bot import views as bot_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bot/events/", bot_views.slack_events_endpoint),
]
