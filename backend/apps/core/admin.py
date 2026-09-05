from django.contrib import admin

from .models import CareerUpdate, Category, Exam, NewsletterSubscriber, Organization, Recruitment

admin.site.register(Organization)
admin.site.register(Category)
@admin.register(Recruitment)
class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "category", "total_vacancies", "location", "published_at", "last_date", "is_active")
    list_filter = ("is_active", "is_featured", "status", "category", "location")
    search_fields = ("title", "organization__name", "qualification", "description")
    ordering = ("-published_at",)
admin.site.register(Exam)
admin.site.register(CareerUpdate)
admin.site.register(NewsletterSubscriber)
