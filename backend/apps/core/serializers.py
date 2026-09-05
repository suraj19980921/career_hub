from django.utils import timezone
from rest_framework import serializers

from .models import CareerUpdate, Category, Exam, NewsletterSubscriber, Organization, Recruitment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug", "icon")


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "short_name", "slug", "icon")


class RecruitmentSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.name")
    organization_icon = serializers.CharField(source="organization.icon")
    category = serializers.CharField(source="category.name")
    last_date = serializers.DateField(format="%d %b %Y")
    status_label = serializers.CharField(source="get_status_display")
    job_status = serializers.SerializerMethodField()
    published_display = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Recruitment
        fields = ("title", "slug", "organization", "organization_icon", "category", "total_vacancies", "qualification", "description", "location", "age_min", "age_max", "application_start_date", "last_date", "status", "status_label", "job_status", "published_at", "published_display", "days_remaining", "application_url")

    def get_job_status(self, obj):
        today = timezone.localdate()
        if obj.application_start_date and obj.application_start_date > today:
            return "upcoming"
        return "closed" if obj.last_date < today else "open"

    def get_published_display(self, obj):
        days = max((timezone.now() - obj.published_at).days, 0)
        if days == 0:
            return "Today"
        return f"{days} day{'s' if days != 1 else ''} ago"

    def get_days_remaining(self, obj):
        return max((obj.last_date - timezone.localdate()).days, 0)


class ExamSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.name")
    organization_icon = serializers.CharField(source="organization.icon")
    exam_date = serializers.DateField(format="%d %b %Y")
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ("title", "slug", "organization", "organization_icon", "exam_type", "exam_date", "status", "days_remaining")

    def get_days_remaining(self, obj):
        return max((obj.exam_date - timezone.localdate()).days, 0)


class CareerUpdateSerializer(serializers.ModelSerializer):
    published_display = serializers.SerializerMethodField()

    class Meta:
        model = CareerUpdate
        fields = ("title", "slug", "update_type", "description", "published_at", "published_display")

    def get_published_display(self, obj):
        delta = timezone.now() - obj.published_at
        minutes = max(int(delta.total_seconds() // 60), 0)
        if minutes < 60:
            return f"{minutes or 1} min ago"
        if minutes < 1440:
            return f"{minutes // 60} hour ago"
        return obj.published_at.strftime("%d %b %Y")


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)

    def create(self, validated_data):
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=validated_data["email"])
        if not created:
            if subscriber.is_active:
                raise serializers.ValidationError({"email": "This email is already subscribed."})
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save(update_fields=("is_active", "unsubscribed_at"))
        return subscriber
