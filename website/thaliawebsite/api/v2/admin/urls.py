from django.urls import path, include

app_name = "thaliawebsite"

urlpatterns = [
    path("", include("events.api.v2.admin.urls")),
]
