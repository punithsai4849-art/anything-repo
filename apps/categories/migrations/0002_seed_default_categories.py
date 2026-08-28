from django.db import migrations

CATEGORIES_DATA = [
    ("Apps", "apps", "Mobile applications, desktop software, and digital tools", ""),
    ("Books", "books", "Novels, non-fiction, philosophy, literature, and publications", ""),
    ("Companies", "companies", "Enterprises, tech giants, studios, and corporate organizations", ""),
    ("Concepts", "concepts", "Scientific principles, theoretical frameworks, and abstract paradigms", ""),
    ("Diseases & Health", "health", "Medical conditions, wellness topics, and health realities", ""),
    ("Events", "events", "Conferences, tournaments, festivals, and cultural moments", ""),
    ("Experiences", "experiences", "Milestones, journeys, activities, and life events", ""),
    ("Feelings", "feelings", "Human emotions, moods, and psychological states", ""),
    ("Food", "food", "Dishes, culinary creations, ingredients, and recipes", ""),
    ("Games", "games", "Video games, board games, and interactive digital media", ""),
    ("Ideas", "ideas", "Philosophical concepts, movements, and thought experiments", ""),
    ("Movies", "movies", "Feature films, cinema classics, and documentaries", ""),
    ("People", "people", "Public figures, creators, scientists, thinkers, and historical icons", ""),
    ("Places", "places", "Cities, natural wonders, travel destinations, and architectural landmarks", ""),
    ("Products", "products", "Smartphones, hardware, tools, gadgets, and consumer goods", ""),
    ("Restaurants", "restaurants", "Dining establishments, cafes, bistros, and eateries", ""),
    ("Services", "services", "Streaming services, transit, utilities, and platforms", ""),
    ("Songs", "songs", "Musical tracks, singles, compositions, and anthems", ""),
    ("Technology", "technology", "Hardware architectures, AI models, paradigms, and innovations", ""),
    ("Websites", "websites", "Online platforms, web services, and internet culture", ""),
    ("Other", "other", "Anything else under the sun that defies singular categorization", ""),
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    for name, slug, description, icon in CATEGORIES_DATA:
        Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'icon': icon,
            }
        )

def unseed_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    slugs = [c[1] for c in CATEGORIES_DATA]
    Category.objects.filter(slug__in=slugs).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
