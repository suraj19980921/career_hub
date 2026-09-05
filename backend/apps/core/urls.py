from django.urls import path

from .views import health_check, homepage, recruitment_filters, recruitment_list, recruitment_stats, search, subscribe_newsletter


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("v1/homepage/", homepage, name="homepage"),
    path("v1/search/", search, name="search"),
    path("v1/recruitments/", recruitment_list, name="recruitment-list"),
    path("v1/recruitments/stats/", recruitment_stats, name="recruitment-stats"),
    path("v1/recruitments/filters/", recruitment_filters, name="recruitment-filters"),
    path("v1/newsletter/subscribe/", subscribe_newsletter, name="newsletter-subscribe"),
]
