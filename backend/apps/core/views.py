from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import CareerUpdate, Category, Exam, Organization, Recruitment
from .serializers import CareerUpdateSerializer, CategorySerializer, ExamSerializer, NewsletterSubscriptionSerializer, OrganizationSerializer, RecruitmentSerializer


class RecruitmentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET"])
def health_check(request):
    """Return a minimal readiness response for local development and deployment."""
    return Response({"status": "ok"})


@api_view(["GET"])
def homepage(request):
    recruitments = Recruitment.objects.filter(is_active=True, is_featured=True).select_related("organization", "category")[:4]
    exams = Exam.objects.filter(is_active=True, is_featured=True).select_related("organization", "category")[:5]
    updates = CareerUpdate.objects.filter(is_active=True).select_related("related_recruitment", "related_exam")[:5]
    category_items = Category.objects.filter(is_active=True).order_by("name")[:10]
    return Response({
        "quick_access": [
            {"icon": "💼", "title": "Latest Jobs", "detail": f"{Recruitment.objects.filter(is_active=True).count()} active jobs"},
            {"icon": "🏅", "title": "Results", "detail": "Coming soon"},
            {"icon": "▣", "title": "Admit Cards", "detail": "Coming soon"},
            {"icon": "▤", "title": "Answer Keys", "detail": "Coming soon"},
        ],
        "latest_recruitments": RecruitmentSerializer(recruitments, many=True).data,
        "categories": CategorySerializer(category_items, many=True).data,
        "upcoming_exams": ExamSerializer(exams, many=True).data,
        "latest_updates": CareerUpdateSerializer(updates, many=True).data,
        "statistics": [
            {"value": "50L+", "label": "Monthly Users"},
            {"value": "2.5Cr+", "label": "Page Views"},
            {"value": "1L+", "label": "Jobs Available"},
            {"value": "500+", "label": "Exams Covered"},
            {"value": "100%", "label": "Authentic Info"},
            {"value": "24×7", "label": "Support"},
        ],
    })


@api_view(["GET"])
def search(request):
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response({"recruitments": [], "exams": []})
    recruitment_items = Recruitment.objects.filter(is_active=True).filter(Q(title__icontains=query) | Q(organization__name__icontains=query)).select_related("organization", "category")[:10]
    exam_items = Exam.objects.filter(is_active=True).filter(Q(title__icontains=query) | Q(organization__name__icontains=query)).select_related("organization", "category")[:10]
    return Response({"recruitments": RecruitmentSerializer(recruitment_items, many=True).data, "exams": ExamSerializer(exam_items, many=True).data})


@api_view(["GET"])
def recruitment_list(request):
    today = timezone.localdate()
    queryset = Recruitment.objects.filter(is_active=True).select_related("organization", "category")
    search_term = request.query_params.get("search", "").strip()
    if search_term:
        queryset = queryset.filter(Q(title__icontains=search_term) | Q(organization__name__icontains=search_term) | Q(description__icontains=search_term))
    category = request.query_params.get("category", "").strip()
    organization = request.query_params.get("organization", "").strip()
    if category:
        queryset = queryset.filter(Q(category__slug__iexact=category) | Q(category__name__iexact=category))
    if organization:
        queryset = queryset.filter(Q(organization__slug__iexact=organization) | Q(organization__name__iexact=organization) | Q(organization__short_name__iexact=organization))
    qualification = request.query_params.get("qualification", "").strip()
    location = request.query_params.get("state", "").strip()
    if qualification:
        queryset = queryset.filter(qualification__icontains=qualification)
    if location:
        queryset = queryset.filter(location__iexact=location)
    job_status = request.query_params.get("status", "").strip().lower()
    if job_status == "open":
        queryset = queryset.filter(last_date__gte=today).filter(Q(application_start_date__lte=today) | Q(application_start_date__isnull=True))
    elif job_status == "upcoming":
        queryset = queryset.filter(application_start_date__gt=today)
    elif job_status == "closed":
        queryset = queryset.filter(last_date__lt=today)
    date_posted = request.query_params.get("date_posted", "").strip().lower()
    ranges = {"24h": 1, "7d": 7, "30d": 30}
    if date_posted in ranges:
        queryset = queryset.filter(published_at__gte=timezone.now() - timedelta(days=ranges[date_posted]))
    ordering = request.query_params.get("ordering", "-published_at").strip().lower()
    allowed_ordering = {"-published_at", "last_date", "-total_vacancies"}
    queryset = queryset.order_by(ordering if ordering in allowed_ordering else "-published_at", "id")
    paginator = RecruitmentPagination()
    page = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(RecruitmentSerializer(page, many=True).data)


@api_view(["GET"])
def recruitment_stats(request):
    today = timezone.localdate()
    active = Recruitment.objects.filter(is_active=True)
    open_jobs = active.filter(last_date__gte=today).filter(Q(application_start_date__lte=today) | Q(application_start_date__isnull=True))
    return Response({
        "total": active.count(),
        "open": open_jobs.count(),
        "upcoming": active.filter(application_start_date__gt=today).count(),
        "closing_soon": open_jobs.filter(last_date__lte=today + timedelta(days=7)).count(),
    })


@api_view(["GET"])
def recruitment_filters(request):
    active = Recruitment.objects.filter(is_active=True)
    return Response({
        "categories": CategorySerializer(Category.objects.filter(is_active=True), many=True).data,
        "organizations": OrganizationSerializer(Organization.objects.filter(is_active=True), many=True).data,
        "qualifications": list(active.exclude(qualification="").order_by("qualification").values_list("qualification", flat=True).distinct()),
        "locations": list(active.exclude(location="").order_by("location").values_list("location", flat=True).distinct()),
    })


@api_view(["POST"])
def subscribe_newsletter(request):
    serializer = NewsletterSubscriptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "You are subscribed to GovCareer Hub updates."}, status=status.HTTP_201_CREATED)
