from datetime import timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import Category, Organization, Recruitment


class Command(BaseCommand):
    help = "Create repeatable, clearly labelled development data for the jobs listing."

    def handle(self, *args, **options):
        call_command("seed_homepage")
        today, now = timezone.localdate(), timezone.now()
        categories = list(Category.objects.filter(is_active=True))
        organizations = list(Organization.objects.filter(is_active=True))
        qualifications = ["10th Pass", "12th Pass", "ITI", "Diploma", "Graduate", "Postgraduate", "Engineering / B.Tech"]
        locations = ["All India", "Delhi", "Uttar Pradesh", "Maharashtra", "Bihar"]
        for index in range(1, 26):
            start_offset = 5 if index % 8 == 0 else -index
            end_offset = -2 if index % 9 == 0 else (index % 28) + 2
            Recruitment.objects.update_or_create(slug=f"demo-listing-job-{index}", defaults={
                "title": f"Demo Government Recruitment {index:02d}", "organization": organizations[index % len(organizations)],
                "category": categories[index % len(categories)], "description": "Clearly labelled demonstration vacancy for testing search and filters.",
                "total_vacancies": 50 + index * 17, "qualification": qualifications[index % len(qualifications)], "location": locations[index % len(locations)],
                "age_min": 18, "age_max": 27 + index % 8, "application_start_date": today + timedelta(days=start_offset),
                "last_date": today + timedelta(days=end_offset), "published_at": now - timedelta(days=index % 35),
                "status": Recruitment.Status.CLOSING if 0 <= end_offset <= 7 else Recruitment.Status.NEW,
                "application_url": "https://example.com/demo-application", "is_featured": index <= 4, "is_active": True,
            })
        self.stdout.write(self.style.SUCCESS("Jobs listing demo data is ready."))
