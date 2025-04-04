from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_auto_20250327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True),
        ),
    ]