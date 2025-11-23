from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from main_service.views.input_view import InputView, MatchView


urlpatterns = [
    path("text/", InputView.as_view(), name="text-endpoint"),
    path("match/", MatchView.as_view(), name="match-endpoint"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]