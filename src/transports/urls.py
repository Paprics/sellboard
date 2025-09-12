from django.urls import path
from django.views.generic import TemplateView

app_name = "transports"

urlpatterns = [
    path("hold/", TemplateView.as_view(template_name="hold.html")),
]
