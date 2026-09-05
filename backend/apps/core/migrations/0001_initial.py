# Generated manually from the initial homepage model definitions.
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(name="Category", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("name", models.CharField(max_length=80, unique=True)), ("slug", models.SlugField(unique=True)),
            ("icon", models.CharField(default="•", max_length=12)), ("description", models.TextField(blank=True)), ("is_active", models.BooleanField(default=True)),
        ], options={"verbose_name_plural": "categories", "ordering": ["name"]}),
        migrations.CreateModel(name="NewsletterSubscriber", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("email", models.EmailField(max_length=254, unique=True)), ("is_active", models.BooleanField(default=True)),
            ("subscribed_at", models.DateTimeField(auto_now_add=True)), ("unsubscribed_at", models.DateTimeField(blank=True, null=True)),
        ], options={"ordering": ["-subscribed_at"]}),
        migrations.CreateModel(name="Organization", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("name", models.CharField(max_length=160, unique=True)), ("short_name", models.CharField(max_length=30, unique=True)), ("slug", models.SlugField(unique=True)),
            ("icon", models.CharField(default="🏛️", max_length=12)), ("description", models.TextField(blank=True)), ("website_url", models.URLField(blank=True)), ("is_active", models.BooleanField(default=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Exam", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("title", models.CharField(max_length=200)), ("slug", models.SlugField(unique=True)), ("exam_type", models.CharField(max_length=100)), ("exam_date", models.DateField()), ("application_last_date", models.DateField(blank=True, null=True)), ("status", models.CharField(default="Scheduled", max_length=30)), ("is_featured", models.BooleanField(default=False)), ("is_active", models.BooleanField(default=True)),
            ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="exams", to="core.category")), ("organization", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="exams", to="core.organization")),
        ], options={"ordering": ["exam_date"]}),
        migrations.CreateModel(name="Recruitment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("title", models.CharField(max_length=200)), ("slug", models.SlugField(unique=True)), ("total_vacancies", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])), ("qualification", models.CharField(max_length=150)), ("last_date", models.DateField()), ("status", models.CharField(choices=[("new", "New"), ("featured", "Featured"), ("closing", "Closing soon")], default="new", max_length=12)), ("application_url", models.URLField(blank=True)), ("published_at", models.DateTimeField()), ("is_featured", models.BooleanField(default=False)), ("is_active", models.BooleanField(default=True)),
            ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="recruitments", to="core.category")), ("organization", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="recruitments", to="core.organization")),
        ], options={"ordering": ["last_date"]}),
        migrations.CreateModel(name="CareerUpdate", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("title", models.CharField(max_length=220)), ("slug", models.SlugField(unique=True)), ("update_type", models.CharField(choices=[("notice", "Notice"), ("result", "Result"), ("admit_card", "Admit card"), ("answer_key", "Answer key"), ("exam_date", "Exam date")], max_length=20)), ("description", models.TextField(blank=True)), ("published_at", models.DateTimeField()), ("is_active", models.BooleanField(default=True)),
            ("related_exam", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updates", to="core.exam")), ("related_recruitment", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updates", to="core.recruitment")),
        ], options={"ordering": ["-published_at"]}),
        migrations.AddIndex(model_name="exam", index=models.Index(fields=["is_active", "is_featured", "exam_date"], name="core_exam_is_acti_cf3bca_idx")),
        migrations.AddIndex(model_name="exam", index=models.Index(fields=["title"], name="core_exam_title_7e3089_idx")),
        migrations.AddIndex(model_name="recruitment", index=models.Index(fields=["is_active", "is_featured", "last_date"], name="core_recrui_is_acti_2e2cbb_idx")),
        migrations.AddIndex(model_name="recruitment", index=models.Index(fields=["title"], name="core_recrui_title_c7bb0a_idx")),
        migrations.AddIndex(model_name="careerupdate", index=models.Index(fields=["is_active", "published_at"], name="core_career_is_acti_855adb_idx")),
    ]
