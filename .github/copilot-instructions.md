# Copilot / AI Agent Instructions for The Filter Shop 🔧

Summary
- This is a Django (4.2) web app that curates and filters products (games initially).
- App root: `thefiltershop/` — the Django project lives in `thefiltershop/thefiltershop/` and the main app is `filtershop_main/`.

Quick start (local dev) ⚡
- Create/activate a Python venv (or use the provided venv in `thefiltershop/`):
  - Windows PowerShell: `.	hefiltershop\Scripts\Activate.ps1`
- Install deps: `pip install -r requirements.txt` (run from repo root)
- Run tests: `cd thefiltershop && python manage.py test`
- Run server: `cd thefiltershop && python manage.py runserver`

  Note: On Windows PowerShell use `.	hefiltershop\Scripts\Activate.ps1` to activate the provided venv (or `python -m venv .venv` and `.\.venv\Scripts\Activate.ps1`).
- Migrations: `cd thefiltershop && python manage.py makemigrations && python manage.py migrate`

Important architecture & conventions 🏗️
- Single Django project with one main app `filtershop_main`.
- `models.BaseModel` centralizes common fields: `name`, `description`, created/updated audit fields.
- Custom user model: `AUTH_USER_MODEL = 'filtershop_main.User'` (check `settings.py`).
- Admin is customized: `filtershop_main.admin.MyAdminSite` registered at `/admin/` (`admin_site` imported in project `urls.py`).
- Admin contains actions that fetch remote data (Steam API) — see `filtershop_main/admin.py`.
- Images uploaded to `MEDIA_ROOT` (default `./media`); model `save()` hooks resize images using Pillow to 300×300.
- Templates group: `filtershop_main/templates/thefiltershop/` and partials under `partials/` (follow these conventions for new pages).

CI & tests 🔁
- GitHub Actions CI: `.github/workflows/django.yml` uses matrix Python (3.9–3.11) and runs `cd thefiltershop && python3 manage.py test` after installing `requirements.txt`.
- Tests use Django `TestCase` and the Django test runner. Always run `python manage.py test` locally before pushing.

External integrations & dependencies ⚙️
- Steam APIs used by admin actions and `filtershop_main/task.py` to populate or fetch game info.
- `requests`, `beautifulsoup4`, and `bs4` are used for web fetching/parsing.
- Postgres is configured in `settings.py` (default DB config points to Postgres). There is a commented SQLite block if you want to run locally without Postgres.
- `django_object_actions` is used to create object actions in admin (see usage in `admin.py`).

Project-specific patterns & gotchas ⚠️
- Audit/author tracking: `created_by` and `last_changed_by` are managed inside admin `save_model` and by `last_changed_by` M2M. Be sure to update these when adding new model actions or custom saves.
- Many `related_name` values use patterns like `"%(app_label)s_%(class)s_related_type"` — preserve these when adding relations to avoid naming collisions.
- `settings.py` contains a hard-coded `SECRET_KEY` and DB credentials for local dev. Avoid committing secrets and be cautious if modifying `settings.py`.
- Media URL handling in some templates/models is non-standard (e.g., manual `image_tag` uses `/../../media/...`). Prefer using Django `{{ MEDIA_URL }}` and proper `ImageField.url` where possible.
- Resizing images happens in model `save()` — large images will be mutated on save; tests and fixtures that add images may need Pillow and a valid image file.

Where to look for examples (code pointers) 🔎
- Admin Steam fetch and image handling examples: `filtershop_main/admin.py` (look for `EntryOnSteam.getDataFromSteam`, `getCapsuleAndHeader`).
- Database models & shared patterns: `filtershop_main/models.py` (BaseModel, Entity, Videogame_common, Sponsor).
- Main URL/API surface: `filtershop_main/urls.py` and views in `filtershop_main/views.py`.
- Tests: `filtershop_main/tests.py` (patterns for model validation tests).
- CI workflow: `.github/workflows/django.yml`.

What an AI agent should do first (prioritized) ✅
1. Run tests locally (`python -m pip install -r requirements.txt` + `cd thefiltershop && python manage.py test`) to establish baseline.
2. Read `filtershop_main/models.py` and `filtershop_main/admin.py` to understand data flows and admin-side ETL (Steam fetch). Use those as canonical examples for changing the data model and remote integrations.
3. When adding features: update models → `makemigrations` → `migrate` → add tests → run full test suite.
4. Use the templates under `templates/thefiltershop` and partials for UI changes.

PR and code review expectations
- Keep changes small and focused (one logical change per PR).
- Include/adjust migrations when changing models.
- Add or update tests demonstrating behavior change.
- Run the test suite locally and ensure CI matrix passes.

If anything is unclear, ask a short question and point to the file you looked at (e.g., "In `filtershop_main/admin.py` I see `getCapsuleAndHeader` — should new image-fetching functions reuse that?" ).

---
Please review and tell me if you want any additional examples or if I should merge this with a different format (shorter/longer). Happy to iterate! ✨