from datetime import timedelta
from urllib.parse import parse_qs, urlparse

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Category, Organization, Recruitment


class RecruitmentListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Railways", slug="railways")
        cls.other_category = Category.objects.create(name="Banking", slug="banking")
        cls.organization = Organization.objects.create(name="Demo Railways", short_name="DR", slug="demo-railways")
        cls.other_organization = Organization.objects.create(name="Demo Bank", short_name="DB", slug="demo-bank")
        today, now = timezone.localdate(), timezone.now()
        for index in range(23):
            Recruitment.objects.create(title=f"Railway Technician {index}", slug=f"railway-{index}", organization=cls.organization,
                category=cls.category, description="Technical government role", total_vacancies=100+index, qualification="Diploma",
                location="All India", application_start_date=today-timedelta(days=2), last_date=today+timedelta(days=10+index), published_at=now-timedelta(days=index))
        Recruitment.objects.create(title="Future Bank Officer", slug="future-bank", organization=cls.other_organization,
            category=cls.other_category, total_vacancies=10, qualification="Graduate", location="Delhi",
            application_start_date=today+timedelta(days=5), last_date=today+timedelta(days=20), published_at=now)
        Recruitment.objects.create(title="Closed Bank Clerk", slug="closed-bank", organization=cls.other_organization,
            category=cls.other_category, total_vacancies=5, qualification="12th Pass", location="Delhi",
            application_start_date=today-timedelta(days=20), last_date=today-timedelta(days=1), published_at=now-timedelta(days=2))

    def setUp(self): self.client = APIClient()
    def results(self, **params): return self.client.get(reverse("recruitment-list"), params).json()
    def test_list_is_paginated(self):
        data=self.results(); self.assertEqual(data["count"],25); self.assertEqual(len(data["results"]),20); self.assertIsNotNone(data["next"])
        second_page = self.results(page=2)
        self.assertEqual(len(second_page["results"]), 5)
        self.assertIsNotNone(second_page["previous"])

    def test_filtered_pagination_preserves_query_parameters(self):
        params = {"category": "railways", "qualification": "Diploma", "status": "open", "ordering": "last_date", "page_size": 10}
        first_page = self.results(**params)
        self.assertEqual(first_page["count"], 23)
        self.assertEqual(len(first_page["results"]), 10)
        next_query = parse_qs(urlparse(first_page["next"]).query)
        for key, value in params.items():
            self.assertEqual(next_query[key], [str(value)])
        self.assertEqual(next_query["page"], ["2"])
        second_page = self.results(**params, page=2)
        self.assertEqual(len(second_page["results"]), 10)
    def test_search_and_filters(self):
        self.assertEqual(self.results(search="technical")["count"],23)
        self.assertEqual(self.results(category="banking")["count"],2)
        self.assertEqual(self.results(organization="demo-bank")["count"],2)
        self.assertEqual(self.results(qualification="Graduate")["count"],1)
        self.assertEqual(self.results(state="Delhi")["count"],2)
        self.assertEqual(self.results(status="upcoming")["count"],1)
        self.assertEqual(self.results(status="closed")["count"],1)
        self.assertGreater(self.results(status="open")["count"],0)
        self.assertGreater(self.results(date_posted="24h")["count"],0)

    def test_all_filters_work_together(self):
        data = self.results(
            search="technical",
            category="railways",
            organization="demo-railways",
            qualification="Diploma",
            state="All India",
            status="open",
            date_posted="7d",
            ordering="-total_vacancies",
        )
        self.assertGreater(data["count"], 0)
        vacancies = [item["total_vacancies"] for item in data["results"]]
        self.assertEqual(vacancies, sorted(vacancies, reverse=True))
        for item in data["results"]:
            self.assertEqual(item["category"], "Railways")
            self.assertEqual(item["organization"], "Demo Railways")
            self.assertEqual(item["qualification"], "Diploma")
            self.assertEqual(item["location"], "All India")
            self.assertEqual(item["job_status"], "open")

    def test_filters_are_case_insensitive(self):
        data = self.results(
            search="tEcHnIcAl",
            category="rAiLwAyS",
            organization="DeMo-RaIlWaYs",
            qualification="dIpLoMa",
            state="aLl InDiA",
            status="OpEn",
            date_posted="7D",
        )
        self.assertGreater(data["count"], 0)
        for item in data["results"]:
            self.assertEqual(item["category"], "Railways")
            self.assertEqual(item["organization"], "Demo Railways")
    def test_sorting_and_invalid_ordering(self):
        data=self.results(ordering="-total_vacancies"); self.assertEqual(data["results"][0]["total_vacancies"],122)
        self.assertEqual(self.results(ordering="not-a-field")["count"],25)
    def test_empty_and_stats(self):
        self.assertEqual(self.results(search="no such job")["results"],[])
        stats=self.client.get(reverse("recruitment-stats")).json(); self.assertEqual(stats["total"],25); self.assertEqual(stats["upcoming"],1)
