from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.AddField(model_name="recruitment", name="description", field=models.TextField(blank=True)),
        migrations.AddField(model_name="recruitment", name="location", field=models.CharField(default="All India", max_length=100)),
        migrations.AddField(model_name="recruitment", name="age_min", field=models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="recruitment", name="age_max", field=models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="recruitment", name="application_start_date", field=models.DateField(blank=True, null=True)),
        migrations.AddIndex(model_name="recruitment", index=models.Index(fields=["is_active", "published_at"], name="core_recrui_is_acti_e1919c_idx")),
    ]
