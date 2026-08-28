# anything...

A modern, universal, open-source platform where users can **discover, rate, review, discuss, contribute information about, and share opinions on anything**.

From movies, books, and technology, to cities, feelings, theories, food, and apps.

> *"If something can be identified, experienced, discussed, or evaluated, it can exist on **anything...**"*

---

## 🌟 Key Capabilities

- **Generic Entity Architecture**: Unified relational data model with PostgreSQL `JSONField` (JSONB) metadata for flexible category-specific schemas.
- **Dynamic Categories**: Pre-configured with Movies, Books, Products, Technology, Apps, Places, Food, Feelings, Concepts, Health, Events, and more.
- **Dynamic Entity Relationships**: Explicit relationship graph (e.g. *Interstellar* `directed_by` *Christopher Nolan*, *iPhone 16 Pro* `created_by` *Apple*).
- **Half-Star Rating & Review Engine**: Standardized 0.5★ to 5.0★ rating scale with ownership protection and unique user constraints.
- **Community Contribution Auditing**: Transparent `EntityEditHistory` recording every community change with contributor attribution and reasons.
- **Universal Social Share Card Studio**: Interactive HTML5 Canvas studio generating Instagram Stories (9:16), Portraits (4:5), and Squares (1:1) in multiple editorial styles with 1-click PNG export & native Web Share API.
- **Content Moderation Workflow**: Report system for Spam, Harassment, and Misinformation managed via Django Admin.
- **Typed REST API**: High-performance OpenAPI endpoints powered by `django-ninja` and Pydantic schemas at `/api/docs`.
- **Neubrutalism & Glassmorphism Design**: High-contrast tactile borders (`2.5px solid #111`), bold offset shadows (`4px 4px 0px #111`), frosted glass surfaces (`backdrop-filter: blur(20px)`), and Apple SF Pro typography.

---

## 🛠️ Technology Stack

- **Backend**: Python, Django, django-ninja, PostgreSQL
- **Frontend**: Vanilla CSS (Neubrutalism + Glassmorphism design system), Apple SF Pro font stack, HTML5 Canvas
- **Database**: PostgreSQL (Relational constraints + JSONB metadata)

---

## 🚀 Quickstart

1. **Clone & Setup Environment**:
   ```bash
   git clone https://github.com/your-username/anything.git
   cd anything
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Migrations & Seed Universal Data**:
   ```bash
   python manage.py migrate
   python manage.py populate_anything
   ```

3. **Start Development Server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

4. **Access Web App & API Docs**:
   - Web App: `http://127.0.0.1:8000/`
   - API Docs: `http://127.0.0.1:8000/api/docs`
   - Admin: `http://127.0.0.1:8000/admin/` (Login: `admin` / `anything123`)

---

## 🧪 Testing

Run the automated test suite:
```bash
python manage.py test
```
