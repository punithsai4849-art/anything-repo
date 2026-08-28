from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.entities.models import Tag, Entity, EntityRelationship
from apps.ratings.models import Rating
from apps.reviews.models import Review

class Command(BaseCommand):
    help = 'Populates anything... with complete real-world entities across all 20 categories with individual user ratings and reviews'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating anything... with comprehensive multi-user community seed data...")

        # 1. Create Seed Community Users
        users_data = [
            ('admin', 'admin@anything.app', 'anything123', True),
            ('maya_explorer', 'maya@example.com', 'anything123', False),
            ('alex_reviewer', 'alex@example.com', 'anything123', False),
            ('claire_cinema', 'claire@example.com', 'anything123', False),
            ('marcus_tech', 'marcus@example.com', 'anything123', False),
            ('sophia_reads', 'sophia@example.com', 'anything123', False),
            ('arjun_travels', 'arjun@example.com', 'anything123', False),
            ('elena_mind', 'elena@example.com', 'anything123', False),
        ]

        seed_users = {}
        for username, email, password, is_staff in users_data:
            u, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'is_staff': is_staff, 'is_superuser': is_staff}
            )
            if not u.password:
                u.set_password(password)
                u.save()
            seed_users[username] = u

        # 2. Setup All 20 Categories
        categories_data = [
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
            ("Technology", "technology", "Hardware architectures, AI models, paradigms, and innovations", ""),
            ("Websites", "websites", "Online platforms, web services, and internet culture", ""),
            ("Other", "other", "Anything else under the sun that defies singular categorization", ""),
        ]


        cat_map = {}
        for name, slug, desc, icon in categories_data:
            c, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc, 'icon': icon}
            )
            cat_map[slug] = c

        # 3. Master Entity Catalog (Accurate synopses, tags, images, ratings distribution)
        entities_catalog = [
            # 📱 APPS
            {
                'name': 'Spotify',
                'category': 'apps',
                'description': 'An audio streaming service for music, podcasts, and audiobooks, offering a large catalog across many markets.',
                'image_url': 'https://images.unsplash.com/photo-1614680376593-902f749f7ffc?w=800&auto=format&fit=crop&q=80',
                'tags': ['music', 'streaming', 'podcasts', 'audio'],
                'metadata': {'developer': 'Spotify AB', 'platforms': 'iOS, Android, macOS, Windows, Web', 'pricing': 'Freemium / Premium'},
                'scores': [5.0, 4.5, 4.5, 4.0, 4.5],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'The gold standard for audio streaming', 'The recommendation algorithm and Discover Weekly playlists are unmatched.'),
                    ('maya_explorer', 5.0, 'Seamless cross-device switching', 'Spotify Connect makes transitioning music from phone to speaker effortless.')
                ]
            },
            {
                'name': 'WhatsApp',
                'category': 'apps',
                'description': 'A messaging and calling application that supports text, media sharing, voice calls, and video calls with end-to-end encryption.',
                'image_url': 'https://images.unsplash.com/photo-1611746872915-64382b5c76da?w=800&auto=format&fit=crop&q=80',
                'tags': ['messaging', 'communication', 'social'],
                'metadata': {'developer': 'Meta Platforms', 'security': 'End-to-End Encrypted', 'platforms': 'iOS, Android, Web'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'Essential global communication', 'Reliable even on low-bandwidth cellular networks worldwide.')
                ]
            },
            {
                'name': 'ChatGPT',
                'category': 'apps',
                'description': 'An AI application designed for conversation, writing, learning, analysis, coding, and other reasoning tasks.',
                'image_url': 'https://images.unsplash.com/photo-1677442136019-21780efad99a?w=800&auto=format&fit=crop&q=80',
                'tags': ['AI', 'chatbot', 'productivity', 'technology'],
                'metadata': {'developer': 'OpenAI', 'architecture': 'GPT Models', 'capabilities': 'Voice, Vision, Code Interpreter'},
                'scores': [5.0, 4.5, 5.0, 4.0, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'Transformed my daily workflow', 'Indispensable for drafting, brainstorming code architectures, and distilling complex research.')
                ]
            },

            # 📚 BOOKS
            {
                'name': 'Atomic Habits',
                'category': 'books',
                'description': 'A practical book by James Clear focused on building good habits, breaking bad ones, and improving through small behavioral changes.',
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80',
                'tags': ['habits', 'productivity', 'self-improvement'],
                'metadata': {'author': 'James Clear', 'published_year': 2018, 'pages': '320'},
                'scores': [5.0, 4.5, 4.5, 4.0, 4.5],  # Avg 4.5
                'reviews': [
                    ('sophia_reads', 4.5, 'The compounding effect of 1%', 'Clear explains behavioral feedback loops in an actionable and humane way.')
                ]
            },
            {
                'name': 'Harry Potter and the Philosopher\'s Stone',
                'category': 'books',
                'description': 'A fantasy story about Harry Potter\'s introduction to the wizarding world and the mysteries surrounding the Philosopher\'s Stone.',
                'image_url': 'https://images.unsplash.com/photo-1618666012174-83b441c0bc76?w=800&auto=format&fit=crop&q=80',
                'tags': ['fantasy', 'magic', 'fiction'],
                'metadata': {'author': 'J.K. Rowling', 'published_year': 1997, 'pages': '223'},
                'scores': [5.0, 5.0, 4.5, 4.0, 4.0],  # Avg 4.5
                'reviews': [
                    ('sophia_reads', 5.0, 'Pure childhood wonder', 'The world-building of Hogwarts castle remains unmatched in modern fantasy.')
                ]
            },
            {
                'name': '1984',
                'category': 'books',
                'description': 'A dystopian novel exploring surveillance, authoritarian power, and the control of truth and language.',
                'image_url': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&auto=format&fit=crop&q=80',
                'tags': ['dystopian', 'politics', 'classic'],
                'metadata': {'author': 'George Orwell', 'published_year': 1949, 'pages': '328'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'Chillingly prescient masterwork', 'Orwell\'s examination of doublespeak and psychological subjugation is timeless.')
                ]
            },

            # 🏢 COMPANIES
            {
                'name': 'Apple',
                'category': 'companies',
                'description': 'A technology company known for consumer electronics, software, and digital services including iPhone, Mac, and Apple Silicon.',
                'image_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80',
                'tags': ['technology', 'hardware', 'software'],
                'metadata': {'founded': 1976, 'headquarters': 'Cupertino, California', 'founders': 'Steve Jobs, Steve Wozniak, Ronald Wayne'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'Integration across the hardware-software stack', 'Apple Silicon changed the entire laptop industry regarding battery life and efficiency.')
                ]
            },
            {
                'name': 'Netflix',
                'category': 'companies',
                'description': 'An entertainment company focused on streaming films, series, documentaries, and original content worldwide.',
                'image_url': 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&auto=format&fit=crop&q=80',
                'tags': ['streaming', 'entertainment'],
                'metadata': {'founded': 1997, 'headquarters': 'Los Gatos, California'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('claire_cinema', 4.0, 'Pioneered modern streaming cinema', 'Great international catalog, though content churn is frequent.')
                ]
            },
            {
                'name': 'OpenAI',
                'category': 'companies',
                'description': 'An AI research and product company developing artificial intelligence systems and tools such as GPT-4 and DALL-E.',
                'image_url': 'https://images.unsplash.com/photo-1686191128892-3b37813f07a8?w=800&auto=format&fit=crop&q=80',
                'tags': ['AI', 'research', 'technology'],
                'metadata': {'founded': 2015, 'headquarters': 'San Francisco, California'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'Accelerated the AI revolution', 'Their engineering breakthroughs redefined what human-machine interaction looks like.')
                ]
            },

            # 🧠 CONCEPTS
            {
                'name': 'Artificial Intelligence',
                'category': 'concepts',
                'description': 'The field of creating systems capable of performing tasks associated with human intelligence such as reasoning, learning, and problem solving.',
                'image_url': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&auto=format&fit=crop&q=80',
                'tags': ['technology', 'computing', 'AI'],
                'metadata': {'subfields': 'Machine Learning, Deep Learning, NLP, Robotics'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('elena_mind', 4.5, 'The most impactful paradigm shift of our era', 'Bridges pure mathematics, cognitive science, and computational scalability.')
                ]
            },
            {
                'name': 'Democracy',
                'category': 'concepts',
                'description': 'A system of governance in which people exercise political power directly or through elected representatives.',
                'image_url': 'https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?w=800&auto=format&fit=crop&q=80',
                'tags': ['government', 'society'],
                'metadata': {'origin': 'Ancient Athens', 'core_tenets': 'Voting, Rule of law, Separation of powers'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('alex_reviewer', 4.0, 'Imperfect yet essential', 'Democracy demands active civic participation and vigilant institutions to endure.')
                ]
            },
            {
                'name': 'Time',
                'category': 'concepts',
                'description': 'The concept used to understand the sequence, duration, and progression of events from the past through the present to the future.',
                'image_url': 'https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800&auto=format&fit=crop&q=80',
                'tags': ['philosophy', 'science', 'existence'],
                'metadata': {'physics_view': 'Spacetime dimension (Einstein)', 'nature': 'Arrow of entropy'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('elena_mind', 5.0, 'The ultimate non-renewable resource', 'Our perception of time defines everything from physics equations to our deepest regrets and hopes.')
                ]
            },

            # 🩺 DISEASES & HEALTH (Clarified: Community Perspectives, Not Medical Advice)
            {
                'name': 'Common Cold',
                'category': 'health',
                'description': 'A common viral illness that primarily affects the upper respiratory system.',
                'image_url': '',
                'tags': ['health', 'illness'],
                'metadata': {'nature': 'Viral respiratory condition', 'note': 'Community perspectives are shared personal experiences, not medical guidance.'},
                'scores': [2.0, 2.0, 2.0],  # Avg 2.0
                'reviews': [
                    ('alex_reviewer', 2.0, 'Inconvenient and draining', 'Hydration, steam inhalation, and extra sleep are the only things that truly help.')
                ]
            },
            {
                'name': 'Diabetes',
                'category': 'health',
                'description': 'A group of metabolic conditions involving problems with blood glucose regulation.',
                'image_url': '',
                'tags': ['health', 'medical'],
                'metadata': {'types': 'Type 1, Type 2, Gestational', 'management': 'Continuous glucose monitoring, nutrition, insulin'},
                'scores': [2.5, 2.5, 2.5],  # Avg 2.5
                'reviews': [
                    ('maya_explorer', 2.5, 'Demands constant daily discipline', 'Continuous glucose monitors (CGMs) have made daily management significantly easier.')
                ]
            },
            {
                'name': 'Mental Health',
                'category': 'health',
                'description': 'A broad concept relating to emotional, psychological, and social well-being.',
                'image_url': '',
                'tags': ['psychology', 'wellbeing'],
                'metadata': {'pillars': 'Therapy, Sleep, Physical activity, Connection', 'stigma': 'Actively improving in modern culture'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('elena_mind', 4.0, 'Equally vital to physical health', 'Normalizing open dialogue and setting emotional boundaries changes everything.')
                ]
            },

            # 🎪 EVENTS
            {
                'name': 'FIFA World Cup',
                'category': 'events',
                'description': 'An international football tournament featuring national teams from around the world.',
                'image_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&auto=format&fit=crop&q=80',
                'tags': ['football', 'sports'],
                'metadata': {'frequency': 'Every 4 years', 'governing_body': 'FIFA', 'global_viewership': 'Over 3.5 Billion'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('arjun_travels', 5.0, 'Global euphoria and unity', 'Nothing captures the world\'s collective heartbeat quite like a World Cup knockout match.')
                ]
            },
            {
                'name': 'Apple WWDC',
                'category': 'events',
                'description': 'Apple\'s developer conference focused on software platforms, tools, and technology announcements.',
                'image_url': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&auto=format&fit=crop&q=80',
                'tags': ['Apple', 'developers'],
                'metadata': {'location': 'Cupertino, California', 'focus': 'iOS, macOS, visionOS, Swift'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('marcus_tech', 4.0, 'The benchmark for tech keynotes', 'State of the Union sessions and deep API dives provide great roadmaps for developers.')
                ]
            },
            {
                'name': 'Comic-Con',
                'category': 'events',
                'description': 'A convention centered around comics, films, television, games, and popular culture.',
                'image_url': 'https://images.unsplash.com/photo-1563089145-599997674d42?w=800&auto=format&fit=crop&q=80',
                'tags': ['entertainment', 'culture'],
                'metadata': {'flagship_location': 'San Diego, California', 'activities': 'Panels, Cosplay, Exclusive reveals'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('claire_cinema', 4.5, 'A celebration of storytelling and community', 'The energy in Hall H during trailer drops is electric.')
                ]
            },

            # ✨ EXPERIENCES
            {
                'name': 'Solo Travel',
                'category': 'experiences',
                'description': 'The experience of traveling independently and making decisions without companions.',
                'image_url': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&auto=format&fit=crop&q=80',
                'tags': ['travel', 'independence'],
                'metadata': {'benefits': 'Self-reliance, Spontaneity, Cultural immersion'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'Unlocks genuine confidence', 'Being solely responsible for your itinerary teaches you how to embrace serendipity.')
                ]
            },
            {
                'name': 'First Day at College',
                'category': 'experiences',
                'description': 'The experience of beginning a new phase of academic and social life.',
                'image_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&auto=format&fit=crop&q=80',
                'tags': ['education', 'memories'],
                'metadata': {'life_stage': 'Transition to young adulthood', 'emotions': 'Nervousness, Excitement'},
                'scores': [3.5, 3.5, 3.5],  # Avg 3.5
                'reviews': [
                    ('maya_explorer', 3.5, 'A whirlwind of nerves and possibilities', 'Overwhelming in the morning, exciting by late evening.')
                ]
            },
            {
                'name': 'Working From Home',
                'category': 'experiences',
                'description': 'The experience of performing professional work remotely rather than from a traditional workplace.',
                'image_url': 'https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=800&auto=format&fit=crop&q=80',
                'tags': ['work', 'remote'],
                'metadata': {'advantages': 'Zero commute, Flexible hours', 'challenges': 'Work-life boundaries'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('marcus_tech', 4.0, 'Regained 2 hours of life every day', 'Eliminating the commute was huge, though staying disciplined with shutdown time is crucial.')
                ]
            },

            # 💭 FEELINGS
            {
                'name': 'Happiness',
                'category': 'feelings',
                'description': 'A feeling commonly associated with pleasure, satisfaction, and well-being.',
                'image_url': '',
                'tags': ['emotion', 'positive'],
                'metadata': {'neurotransmitters': 'Dopamine, Serotonin, Oxytocin', 'philosophy': 'Eudaimonia vs Hedonia'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('elena_mind', 5.0, 'Found in presence, not pursuit', 'Happiness isn\'t a finish line; it\'s the warmth of paying attention to the present.')
                ]
            },
            {
                'name': 'Nostalgia',
                'category': 'feelings',
                'description': 'A sentimental feeling connected to memories or experiences from the past.',
                'image_url': '',
                'tags': ['memories', 'emotion'],
                'metadata': {'nature': 'Bittersweet emotional longing', 'triggers': 'Music, Scents, Old photographs'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('sophia_reads', 4.5, 'Bittersweet and comforting', 'Hearing an album from 2012 can instantly teleport you back in time.')
                ]
            },
            {
                'name': 'Loneliness',
                'category': 'feelings',
                'description': 'A feeling of isolation or a lack of meaningful social connection.',
                'image_url': '',
                'tags': ['emotion', 'social'],
                'metadata': {'psychology': 'Evolutionary signal for connection', 'contrast': 'Solitude (positive) vs Loneliness'},
                'scores': [2.5, 2.5, 2.5],  # Avg 2.5
                'reviews': [
                    ('elena_mind', 2.5, 'Painful but instructive', 'It acts as an emotional appetite reminding us of how deeply we need community.')
                ]
            },

            # 🍕 FOOD
            {
                'name': 'Pizza',
                'category': 'food',
                'description': 'A dish built around baked dough and toppings such as cheese, vegetables, or meat.',
                'image_url': 'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=800&auto=format&fit=crop&q=80',
                'tags': ['Italian', 'cheese'],
                'metadata': {'origin': 'Naples, Italy', 'styles': 'Neapolitan, New York, Detroit, Roman'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'The perfect culinary comfort', 'Wood-fired crust with blistered leopard spots and fresh basil is unbeatable.')
                ]
            },
            {
                'name': 'Biryani',
                'category': 'food',
                'description': 'A South Asian rice dish prepared with spices and ingredients such as meat or vegetables.',
                'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&auto=format&fit=crop&q=80',
                'tags': ['Indian', 'rice', 'spicy'],
                'metadata': {'famous_styles': 'Hyderabadi Dum, Lucknowi, Thalassery, Kolkata'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('arjun_travels', 5.0, 'The pinnacle of rice craftsmanship', 'The aroma of saffron, fried onions, and marinated mutton steamed in dum is magical.')
                ]
            },
            {
                'name': 'Sushi',
                'category': 'food',
                'description': 'A Japanese dish commonly combining vinegared rice with ingredients such as seafood or vegetables.',
                'image_url': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&auto=format&fit=crop&q=80',
                'tags': ['Japanese', 'seafood'],
                'metadata': {'styles': 'Nigiri, Sashimi, Maki, Temaki', 'key_element': 'Seasoned Shari rice'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('maya_explorer', 4.0, 'Precision and freshness', 'The subtle balance of vinegared rice and high-grade otoro tuna is sublime.')
                ]
            },

            # 🎮 GAMES
            {
                'name': 'Minecraft',
                'category': 'games',
                'description': 'A sandbox game centered around exploration, building, survival, and creativity.',
                'image_url': 'https://images.unsplash.com/photo-1627856014754-2907e2355324?w=800&auto=format&fit=crop&q=80',
                'tags': ['sandbox', 'creative'],
                'metadata': {'developer': 'Mojang Studios', 'initial_release': 2011, 'genre': 'Sandbox Survival'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('marcus_tech', 5.0, 'Infinite digital lego', 'The most liberating sandbox ever created. Redstone computing alone is a marvel.')
                ]
            },
            {
                'name': 'Grand Theft Auto V',
                'category': 'games',
                'description': 'An open-world action game set in a fictionalized Southern California.',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80',
                'tags': ['open-world', 'action'],
                'metadata': {'developer': 'Rockstar Games', 'setting': 'Los Santos & Blaine County'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'Unrivaled satirical world design', 'The attention to ambient dialogue, radio stations, and open-world density set a high watermark.')
                ]
            },
            {
                'name': 'The Last of Us',
                'category': 'games',
                'description': 'A story-driven game following characters navigating a dangerous post-pandemic world.',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800&auto=format&fit=crop&q=80',
                'tags': ['story', 'survival'],
                'metadata': {'developer': 'Naughty Dog', 'characters': 'Joel, Ellie', 'composer': 'Gustavo Santaolalla'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('claire_cinema', 5.0, 'A masterclass in interactive drama', 'The emotional weight of Joel and Ellie\'s journey transcends the video game medium.')
                ]
            },

            # 💡 IDEAS
            {
                'name': 'Four-Day Workweek',
                'category': 'ideas',
                'description': 'The idea of reducing the standard working week while maintaining productivity or compensation.',
                'image_url': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&auto=format&fit=crop&q=80',
                'tags': ['work', 'productivity'],
                'metadata': {'trials': 'UK 4-Day Pilot, Iceland Trials', 'reported_outcomes': 'Reduced burnout, Maintained output'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'The logical evolution of labor', '3-day weekends give people time to recharge, leading to sharper focus on work days.')
                ]
            },
            {
                'name': 'Universal Basic Income',
                'category': 'ideas',
                'description': 'The idea of providing people with a regular income regardless of employment status.',
                'image_url': 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800&auto=format&fit=crop&q=80',
                'tags': ['economics', 'society'],
                'metadata': {'advocates': 'Milton Friedman, Martin Luther King Jr., Tech leaders'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('alex_reviewer', 4.0, 'Crucial safety net for the automation era', 'Provides dignity and security, though funding mechanisms remain heavily debated.')
                ]
            },
            {
                'name': 'Minimalism',
                'category': 'ideas',
                'description': 'An approach focused on reducing unnecessary possessions, complexity, or consumption.',
                'image_url': 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?w=800&auto=format&fit=crop&q=80',
                'tags': ['lifestyle', 'simplicity'],
                'metadata': {'philosophy': 'Intentional living', 'focus': 'Clarity over clutter'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('sophia_reads', 4.5, 'Mental clarity through intentionality', 'Less stuff means fewer decisions and more energy for creative work.')
                ]
            },

            # 🎬 MOVIES
            {
                'name': 'Interstellar',
                'category': 'movies',
                'description': 'A science-fiction story about astronauts searching for a future home for humanity as Earth faces environmental collapse.',
                'image_url': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
                'tags': ['sci-fi', 'space'],
                'metadata': {'release_year': 2014, 'runtime': '169 min', 'director': 'Christopher Nolan'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('claire_cinema', 5.0, 'A monumental achievement in sci-fi', 'The docking scene set to Hans Zimmer’s organ score is one of the greatest moments in modern cinema.')
                ]
            },
            {
                'name': 'RRR',
                'category': 'movies',
                'description': 'An Indian period action drama centered on a fictional friendship between two revolutionaries fighting British colonial rule.',
                'image_url': 'https://image.tmdb.org/t/p/w500/nEuVPn1d595c5w25pA88yvP1S2q.jpg',
                'tags': ['Indian cinema', 'action'],
                'metadata': {'release_year': 2022, 'runtime': '187 min', 'director': 'S.S. Rajamouli'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'Pure cinematic adrenaline and spectacle', 'S.S. Rajamouli understands epic scale, visual grandeur, and genuine emotional sincerity.')
                ]
            },
            {
                'name': 'The Shawshank Redemption',
                'category': 'movies',
                'description': 'A drama about hope, friendship, and survival within the American prison system.',
                'image_url': 'https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg',
                'tags': ['drama', 'friendship'],
                'metadata': {'release_year': 1994, 'runtime': '142 min', 'director': 'Frank Darabont'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('claire_cinema', 5.0, 'Hope is a good thing, maybe the best of things', 'The narration by Morgan Freeman and the patience of the narrative create pure magic.')
                ]
            },

            # 👤 PEOPLE
            {
                'name': 'A. R. Rahman',
                'category': 'people',
                'description': 'An Indian composer and musician known for revolutionary work across Indian and international cinema.',
                'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop&q=80',
                'tags': ['music', 'composer'],
                'metadata': {'profession': 'Composer, Music Producer, Singer', 'accolades': '2 Academy Awards, 2 Grammy Awards, BAFTA'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('arjun_travels', 5.0, 'The Mozart of Madras', 'His blending of Eastern classical music with electronic soundscapes redefined modern film scoring.')
                ]
            },
            {
                'name': 'Christopher Nolan',
                'category': 'people',
                'description': 'A filmmaker known for large-scale, visually ambitious, and concept-driven films.',
                'image_url': 'https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3Z5.jpg',
                'tags': ['director', 'cinema'],
                'metadata': {'profession': 'Film Director, Producer, Screenwriter', 'notable_works': 'Oppenheimer, Interstellar, The Dark Knight'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('claire_cinema', 4.5, 'Master of practical scale and tension', 'His commitment to IMAX 70mm film and non-linear narrative architecture is inspiring.')
                ]
            },
            {
                'name': 'Satya Nadella',
                'category': 'people',
                'description': 'A technology executive known for transforming and leading Microsoft into cloud and AI leadership.',
                'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&auto=format&fit=crop&q=80',
                'tags': ['technology', 'business'],
                'metadata': {'role': 'Chairman & CEO of Microsoft', 'birthplace': 'Hyderabad, India'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'Empathy-driven corporate transformation', 'Shifted Microsoft\'s culture from "know-it-all" to "learn-it-all" with massive success.')
                ]
            },

            # 📍 PLACES
            {
                'name': 'Hyderabad',
                'category': 'places',
                'description': 'A major city in Telangana known for its 400-year history, world-famous biryani, and thriving technology industry.',
                'image_url': 'https://images.unsplash.com/photo-1572445271230-a78b5944a659?w=800&auto=format&fit=crop&q=80',
                'tags': ['India', 'Telangana', 'city'],
                'metadata': {'country': 'India', 'state': 'Telangana', 'landmarks': 'Charminar, Golconda Fort, HITEC City'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'A dynamic harmony of heritage and future', 'The food culture, hospitality, and modern infrastructure make it a wonderful city.')
                ]
            },
            {
                'name': 'Tokyo',
                'category': 'places',
                'description': 'Japan\'s bustling capital and one of the world\'s largest, safest, and most dynamic metropolitan areas.',
                'image_url': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800&auto=format&fit=crop&q=80',
                'tags': ['Japan', 'travel', 'city'],
                'metadata': {'country': 'Japan', 'highlights': 'Shinjuku, Shibuya, Akihabara, Ginza'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('maya_explorer', 5.0, 'Flawless urban infrastructure and culture', 'Spotless streets, incredible ramen, and world-class transit system.')
                ]
            },
            {
                'name': 'Taj Mahal',
                'category': 'places',
                'description': 'A 17th-century white marble mausoleum in Agra, commissioned by Shah Jahan in memory of Mumtaz Mahal and recognized as a UNESCO World Heritage Site.',
                'image_url': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&auto=format&fit=crop&q=80',
                'tags': ['India', 'history', 'architecture'],
                'metadata': {'location': 'Agra, Uttar Pradesh, India', 'commissioned': '1632', 'architect': 'Ustad Ahmad Lahori'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('arjun_travels', 5.0, 'Breathtaking symmetry in white marble', 'Seeing the morning light hit the dome across the Yamuna river is unforgettable.')
                ]
            },

            # 🛍️ PRODUCTS
            {
                'name': 'iPhone',
                'category': 'products',
                'description': 'A revolutionary line of smartphones developed by Apple featuring iOS, Super Retina displays, and advanced camera systems.',
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop&q=80',
                'tags': ['smartphone', 'Apple'],
                'metadata': {'brand': 'Apple', 'os': 'iOS', 'initial_release': 2007},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'Unbeatable longevity and software support', 'Security updates for 6+ years and consistent video recording quality.')
                ]
            },
            {
                'name': 'PlayStation 5',
                'category': 'products',
                'description': 'A home video game console developed by Sony Interactive Entertainment featuring ultra-high speed SSD and DualSense haptics.',
                'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop&q=80',
                'tags': ['gaming', 'console'],
                'metadata': {'brand': 'Sony', 'storage': 'Ultra-high speed NVMe SSD', 'controller': 'DualSense Wireless'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'DualSense controller haptics are game-changing', 'Instant fast travel load times in games like Spider-Man 2 make gaming seamless.')
                ]
            },
            {
                'name': 'AirPods Pro',
                'category': 'products',
                'description': 'Wireless in-ear headphones featuring active noise cancellation, transparency mode, and spatial audio.',
                'image_url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80',
                'tags': ['audio', 'headphones'],
                'metadata': {'brand': 'Apple', 'chip': 'H2 Chip', 'features': 'Active Noise Cancellation, USB-C'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('sophia_reads', 4.0, 'Adaptive Audio transparency is magic', 'Switching seamlessly between ANC in coffee shops and transparency for conversations.')
                ]
            },

            # 🍽️ RESTAURANTS
            {
                'name': 'Paradise',
                'category': 'restaurants',
                'description': 'A historic restaurant brand in Hyderabad renowned globally for authentic Hyderabadi Dum Biryani since 1953.',
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80',
                'tags': ['biryani', 'Hyderabad', 'dining'],
                'metadata': {'established': 1953, 'famous_dish': 'Hyderabadi Mutton Dum Biryani', 'origin': 'Secunderabad'},
                'scores': [4.5, 4.5, 4.0, 4.0],  # Avg 4.2
                'reviews': [
                    ('arjun_travels', 4.5, 'Legendary Hyderabadi institution', 'The Secunderabad flagship serves generous portions with classic aromatic mirchi ka salan.')
                ]
            },
            {
                'name': 'Chutneys',
                'category': 'restaurants',
                'description': 'A celebrated South Indian vegetarian restaurant famous for Steam Dosa and an array of six house chutneys.',
                'image_url': 'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=800&auto=format&fit=crop&q=80',
                'tags': ['South Indian', 'vegetarian', 'dosa'],
                'metadata': {'specialty': 'Guntur Idli, Babai Hotel Idli, Steam Dosa', 'locations': 'Hyderabad, Bangalore'},
                'scores': [4.5, 4.5, 4.5, 4.0],  # Avg 4.4
                'reviews': [
                    ('maya_explorer', 4.5, 'Best Babai Idli and ginger chutney', 'Ghee-roasted idlis served with a variety of fresh chutneys.')
                ]
            },
            {
                'name': 'Pista House',
                'category': 'restaurants',
                'description': 'An iconic culinary house in Hyderabad celebrated for its authentic GI-tagged Hyderabadi Haleem and baked treats.',
                'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop&q=80',
                'tags': ['haleem', 'sweets', 'Hyderabad'],
                'metadata': {'accreditation': 'GI Tagged Haleem', 'established': 1997},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'The undisputed king of Haleem during Ramadan', 'Slow-cooked for 12 hours with pounded meat, wheat, and clarified butter.')
                ]
            },

            # 🛠️ SERVICES
            {
                'name': 'Uber',
                'category': 'services',
                'description': 'A global platform providing on-demand transportation, ride-hailing, mobility, and delivery services.',
                'image_url': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&auto=format&fit=crop&q=80',
                'tags': ['transport', 'mobility'],
                'metadata': {'founded': 2009, 'headquarters': 'San Francisco, California'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('arjun_travels', 4.0, 'Reliable airport transit worldwide', 'Having the same app work seamlessly in 70+ countries takes the friction out of travel.')
                ]
            },
            {
                'name': 'Google Maps',
                'category': 'services',
                'description': 'A mapping and navigation service for discovering places, transit times, and planning routes.',
                'image_url': 'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=800&auto=format&fit=crop&q=80',
                'tags': ['navigation', 'travel'],
                'metadata': {'developer': 'Google', 'features': 'Live traffic, Street View, Transit schedules'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('arjun_travels', 4.5, 'Essential modern utility', 'Accurate traffic predictions and opening hours save hours every week.')
                ]
            },

            # 💻 TECHNOLOGY
            {
                'name': 'Virtual Reality',
                'category': 'technology',
                'description': 'Technology that creates immersive simulated environments for gaming, training, and spatial computing.',
                'image_url': 'https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=800&auto=format&fit=crop&q=80',
                'tags': ['VR', 'immersive'],
                'metadata': {'key_devices': 'Apple Vision Pro, Meta Quest 3, PlayStation VR2'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('marcus_tech', 4.0, 'Spatial computing has arrived', 'The immersion in flight simulators and 3D architectural visualization is astonishing.')
                ]
            },
            {
                'name': '5G',
                'category': 'technology',
                'description': 'A generation of mobile network technology designed for high speed, low latency, and massive device connectivity.',
                'image_url': 'https://images.unsplash.com/photo-1562774053-701939374585?w=800&auto=format&fit=crop&q=80',
                'tags': ['network', 'mobile'],
                'metadata': {'spectrum': 'Sub-6 GHz, mmWave', 'peak_speed': 'Up to 10 Gbps'},
                'scores': [4.0, 4.0, 4.0],  # Avg 4.0
                'reviews': [
                    ('marcus_tech', 4.0, 'Blazing download speeds on the go', 'Streaming lossless audio and 4K video anywhere without buffering.')
                ]
            },

            # 🌐 WEBSITES
            {
                'name': 'Wikipedia',
                'category': 'websites',
                'description': 'A collaboratively created online encyclopedia covering a wide range of human knowledge in hundreds of languages.',
                'image_url': 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800&auto=format&fit=crop&q=80',
                'tags': ['knowledge', 'education'],
                'metadata': {'founded': 2001, 'model': 'Non-profit Wikimedia Foundation', 'languages': 'Over 300'},
                'scores': [5.0, 5.0, 5.0],  # Avg 5.0
                'reviews': [
                    ('sophia_reads', 5.0, 'The crown jewel of the open internet', 'Ad-free, community-governed, and the first place we all go to learn about anything.')
                ]
            },
            {
                'name': 'YouTube',
                'category': 'websites',
                'description': 'A platform for uploading, watching, and sharing video content across music, education, tutorials, and entertainment.',
                'image_url': 'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&auto=format&fit=crop&q=80',
                'tags': ['video', 'creators'],
                'metadata': {'parent': 'Google', 'founded': 2005, 'video_hours_uploaded': '500+ hours every minute'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('alex_reviewer', 4.5, 'The world\'s greatest learning library', 'From DIY repairs to MIT lectures, any skill can be learned here for free.')
                ]
            },
            {
                'name': 'GitHub',
                'category': 'websites',
                'description': 'A cloud platform for hosting, collaborating on, and managing software projects using Git version control.',
                'image_url': 'https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&auto=format&fit=crop&q=80',
                'tags': ['programming', 'open-source'],
                'metadata': {'parent': 'Microsoft', 'founded': 2008, 'features': 'Pull Requests, Actions, Copilot'},
                'scores': [5.0, 4.5, 4.5, 4.0],  # Avg 4.5
                'reviews': [
                    ('marcus_tech', 4.5, 'The home of modern software development', 'Pull requests, CI/CD Actions, and open-source collaboration made programming global.')
                ]
            }
        ]

        # 4. Populate Entities & Ratings
        created_entities = {}
        rating_users_pool = list(seed_users.values())

        for data in entities_catalog:
            cat_obj = cat_map.get(data['category'], cat_map['other'])
            from django.utils.text import slugify
            import os
            slug_key = slugify(data['name'])
            local_media_path = f'entities/{slug_key}.jpg'
            has_local = os.path.exists(os.path.join('media', local_media_path))

            entity, _ = Entity.objects.get_or_create(
                name=data['name'],
                category=cat_obj,
                defaults={
                    'description': data['description'],
                    'primary_image': local_media_path if has_local else None,
                    'primary_image_url': data.get('image_url', ''),
                    'metadata': data.get('metadata', {}),
                    'created_by': seed_users['admin']
                }
            )
            if has_local and not entity.primary_image:
                entity.primary_image = local_media_path
                entity.save()
            created_entities[data['name']] = entity


            # Tags
            for t_name in data.get('tags', []):
                clean_t = t_name.strip().lower()
                if clean_t:
                    t_obj, _ = Tag.objects.get_or_create(name=clean_t)
                    entity.tags.add(t_obj)

            # Insert Individual Ratings (Multi-user distribution)
            scores = data.get('scores', [4.5, 4.0])
            for i, score in enumerate(scores):
                rater = rating_users_pool[i % len(rating_users_pool)]
                Rating.objects.update_or_create(
                    user=rater,
                    entity=entity,
                    defaults={'score': score}
                )

            # Insert Reviews
            for author_uname, rev_score, rev_title, rev_content in data.get('reviews', []):
                author = seed_users.get(author_uname, seed_users['alex_reviewer'])
                r_obj = Rating.objects.filter(user=author, entity=entity).first()
                if not r_obj:
                    r_obj = Rating.objects.create(user=author, entity=entity, score=rev_score)
                
                Review.objects.update_or_create(
                    user=author,
                    entity=entity,
                    defaults={
                        'title': rev_title,
                        'content': rev_content,
                        'rating': r_obj
                    }
                )

        # 5. Entity Relationships Graph
        relationships_data = [
            ('Interstellar', 'Christopher Nolan', 'directed_by'),
            ('iPhone', 'Apple', 'created_by'),
            ('ChatGPT', 'OpenAI', 'developed_by'),
            ('Spotify', 'Music', 'related_to'),
            ('Hyderabad', 'Taj Mahal', 'located_in'),
            ('A. R. Rahman', 'RRR', 'inspired_by'),
            ('Satya Nadella', 'Hyderabad', 'associated_with'),
        ]

        for src, tgt, r_type in relationships_data:
            if src in created_entities and tgt in created_entities:
                EntityRelationship.objects.get_or_create(
                    source_entity=created_entities[src],
                    target_entity=created_entities[tgt],
                    relationship_type=r_type,
                    defaults={'created_by': seed_users['admin']}
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully populated {len(entities_catalog)} entities with multi-user ratings and reviews!"))
