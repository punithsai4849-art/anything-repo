from django.db import migrations

def add_songs_category(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.get_or_create(
        slug='songs',
        defaults={
            'name': 'Songs',
            'description': 'Musical tracks, singles, compositions, and anthems',
            'icon': '',
        }
    )

def remove_songs_category(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.filter(slug='songs').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_seed_default_categories'),
    ]

    operations = [
        migrations.RunPython(add_songs_category, remove_songs_category),
    ]
