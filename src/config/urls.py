# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("auth/", include("accounts.urls")),
    path("transports/", include("transports.urls")),
]

# DEBUG TOOLBAR
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
