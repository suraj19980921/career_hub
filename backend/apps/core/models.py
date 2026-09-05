from django.core.validators import MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    name = models.CharField(max_length=160, unique=True)
    short_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=12, default="🏛️")
    description = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short_name


class Category(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=12, default="•")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recruitment(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        FEATURED = "featured", "Featured"
        CLOSING = "closing", "Closing soon"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="recruitments")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="recruitments")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    total_vacancies = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    qualification = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, default="All India")
    age_min = models.PositiveSmallIntegerField(null=True, blank=True)
    age_max = models.PositiveSmallIntegerField(null=True, blank=True)
    application_start_date = models.DateField(null=True, blank=True)
    last_date = models.DateField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    application_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_date"]
        indexes = [
            models.Index(fields=["is_active", "is_featured", "last_date"]),
            models.Index(fields=["title"]),
            models.Index(fields=["is_active", "published_at"]),
        ]

    def __str__(self):
        return self.title


class Exam(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="exams")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="exams")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    exam_type = models.CharField(max_length=100)
    exam_date = models.DateField()
    application_last_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, default="Scheduled")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["exam_date"]
        indexes = [models.Index(fields=["is_active", "is_featured", "exam_date"]), models.Index(fields=["title"])]

    def __str__(self):
        return self.title


class CareerUpdate(TimeStampedModel):
    class UpdateType(models.TextChoices):
        NOTICE = "notice", "Notice"
        RESULT = "result", "Result"
        ADMIT_CARD = "admit_card", "Admit card"
        ANSWER_KEY = "answer_key", "Answer key"
        EXAM_DATE = "exam_date", "Exam date"

    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    update_type = models.CharField(max_length=20, choices=UpdateType.choices)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    related_recruitment = models.ForeignKey(Recruitment, null=True, blank=True, on_delete=models.SET_NULL, related_name="updates")
    related_exam = models.ForeignKey(Exam, null=True, blank=True, on_delete=models.SET_NULL, related_name="updates")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["is_active", "published_at"])]

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
