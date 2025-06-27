from django.urls import path
from .views import PublicDataView, ProtectedDataView, CreateTelegramUserView

urlpatterns = [
    path("public/", PublicDataView.as_view(), name="public-data"),
    path("protected/", ProtectedDataView.as_view(), name="protected-data"),
    path(
        "create-telegram-user/",
        CreateTelegramUserView.as_view(),
        name="create-telegram-user",
    ),
]
