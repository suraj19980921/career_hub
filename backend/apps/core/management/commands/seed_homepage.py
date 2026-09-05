from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import CareerUpdate, Category, Exam, Organization, Recruitment


class Command(BaseCommand):
    help = "Create repeatable clearly labelled development data for the homepage."

    def handle(self, *args, **options):
        categories = [
            ("Railways", "railways", "🚆"), ("Banking", "banking", "🏦"), ("Defence", "defence", "🛡"),
            ("Teaching", "teaching", "🎓"), ("SSC", "ssc", "●"), ("Police", "police", "👮"),
            ("State Government", "state-government", "🏛"), ("Engineering", "engineering", "⚙"),
            ("Healthcare", "healthcare", "♥"),
        ]
        category_map = {}
        for name, slug, icon in categories:
            category_map[slug], _ = Category.objects.update_or_create(slug=slug, defaults={"name": name, "icon": icon, "is_active": True})

        organizations = [
            ("Demo Staff Selection Commission", "Demo SSC", "demo-ssc", "🏛️"),
            ("Demo Indian Railways", "Demo Railways", "demo-railways", "🚉"),
            ("Demo Uttar Pradesh Police", "Demo UP Police", "demo-up-police", "👮"),
            ("Demo Intelligence Bureau", "Demo IB", "demo-ib", "✺"),
        ]
        organization_map = {}
        for name, short_name, slug, icon in organizations:
            organization_map[slug], _ = Organization.objects.update_or_create(slug=slug, defaults={"name": name, "short_name": short_name, "icon": icon, "is_active": True})

        today = timezone.localdate()
        now = timezone.now()
        recruitment_specs = [
            ("demo-ssc-cgl", "Demo SSC Graduate Recruitment", "demo-ssc", "ssc", 120, "Graduation", 14),
            ("demo-railway-technician", "Demo Railway Technician", "demo-railways", "railways", 80, "10th / ITI / Diploma", 21),
            ("demo-police-constable", "Demo Police Constable Recruitment", "demo-up-police", "police", 60, "12th Pass", 28),
            ("demo-ib-acio", "Demo Intelligence Officer Recruitment", "demo-ib", "ssc", 25, "Graduation", 35),
        ]
        recruitment_map = {}
        for slug, title, org, category, vacancies, qualification, days in recruitment_specs:
            recruitment_map[slug], _ = Recruitment.objects.update_or_create(slug=slug, defaults={"title": title, "organization": organization_map[org], "category": category_map[category], "total_vacancies": vacancies, "qualification": qualification, "last_date": today + timedelta(days=days), "status": Recruitment.Status.NEW, "published_at": now - timedelta(days=2), "is_featured": True, "is_active": True})

        exam_specs = [
            ("demo-ssc-chsl", "Demo SSC CHSL", "demo-ssc", "ssc", "Tier I Exam", 20),
            ("demo-bank-po", "Demo Bank PO", "demo-railways", "banking", "Prelims Exam", 27),
            ("demo-rrb-ntpc", "Demo RRB NTPC", "demo-railways", "railways", "CBT I Exam", 34),
            ("demo-state-pet", "Demo State PET", "demo-up-police", "state-government", "PET Exam", 41),
            ("demo-ssc-mts", "Demo SSC MTS", "demo-ssc", "ssc", "Computer Based Test", 48),
        ]
        exam_map = {}
        for slug, title, org, category, exam_type, days in exam_specs:
            exam_map[slug], _ = Exam.objects.update_or_create(slug=slug, defaults={"title": title, "organization": organization_map[org], "category": category_map[category], "exam_type": exam_type, "exam_date": today + timedelta(days=days), "status": "Scheduled", "is_featured": True, "is_active": True})

        update_specs = [
            ("demo-admit-card", "Demo Technician admit-card update", CareerUpdate.UpdateType.ADMIT_CARD, 2),
            ("demo-result", "Demo graduate recruitment result update", CareerUpdate.UpdateType.RESULT, 20),
            ("demo-answer-key", "Demo constable answer-key update", CareerUpdate.UpdateType.ANSWER_KEY, 45),
            ("demo-exam-date", "Demo PET exam-date update", CareerUpdate.UpdateType.EXAM_DATE, 90),
            ("demo-notice", "Demo recruitment notification update", CareerUpdate.UpdateType.NOTICE, 120),
        ]
        for slug, title, update_type, minutes in update_specs:
            CareerUpdate.objects.update_or_create(slug=slug, defaults={"title": title, "update_type": update_type, "description": "Development sample content — not a live government notice.", "published_at": now - timedelta(minutes=minutes), "is_active": True})
        self.stdout.write(self.style.SUCCESS("Homepage development data is ready."))
