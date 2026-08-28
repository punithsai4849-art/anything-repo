# Contributing to anything...

We welcome community contributions to **anything...**! Whether you are adding new categories, fixing a bug, proposing a design improvement, or adding a new feature, here is how you can get involved.

---

## 🛠️ Contribution Guidelines

1. **Keep it Universal**: The platform must remain generic and capable of handling physical products, movies, books, places, feelings, ideas, and software without hardcoded category limitations.
2. **Follow the Modular Monolith Architecture**:
   - `apps/categories`: Category models and metadata schemas.
   - `apps/entities`: Generic Entity, Tag, EntityRelationship, and EntityMedia models.
   - `apps/ratings`: Half-star rating system.
   - `apps/reviews`: User review system.
   - `apps/contributions`: Contribution audit logging.
   - `apps/moderation`: Reporting and trust & safety workflow.
   - `apps/sharing`: Social Share Card generator.
3. **Design Aesthetics**:
   - Brand Color: `#FF4433` (Brand Red-Orange)
   - Apple SF Pro System Typography
   - Neubrutalism & Glassmorphism Fusion (`2.5px solid #111` borders, hard offset shadows, frosted glass blur).

---

## 🧪 Testing Your Changes

Before submitting your pull request, ensure all tests pass:
```bash
python manage.py test
```
