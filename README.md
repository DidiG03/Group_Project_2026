# Sky Engineering Teams Portal

Group coursework project for **5COSC021W Software Development Group Project (2025/26)**.

This Django web app replaces a shared spreadsheet that Sky engineering managers were using to keep track of their teams. It is an internal portal where any logged-in user can search teams, browse the org structure, schedule meetings, message colleagues, run reports, and view simple charts.

## What the app does

- Self-service registration, login, profile editing, password change, password reset.
- Dashboard with KPI cards (departments, teams, active teams, unread notifications) and a search box that queries teams, departments and managers in one go.
- Team pages with mission, manager, members, Slack/Teams channel, repository link, lifecycle status (active / restructured / disbanded) and upstream/downstream dependencies.
- "Email Team" and "Schedule Meeting" buttons on every team page that pre-fill the message/meeting form with the right team selected.
- Inbox / Sent / Drafts for internal messages, with notifications when a new message lands.
- Schedule page that splits meetings into Upcoming, Weekly and Monthly cards.
- Reports page with CSV (Excel-compatible) and PDF export of the team summary.
- Analytics page with two Chart.js charts (departments by team count, managers by team count).
- In-app notification stream + navbar badge.
- Read-only audit log at `/audit-log/` showing every create/update/delete with the actor and timestamp.
- Custom 404 page.
- Django admin for power users.

## Tech stack

- Python 3.11+ (the `.venv` was created with the version installed by the University)
- Django 6.0
- SQLite (file-based, ships with the repo as `db.sqlite3`)
- Bootstrap 5 + a small custom stylesheet (`static/css/site.css`)
- Chart.js (loaded from CDN on the analytics page)
- ReportLab (for PDF exports)

The whole stack is server-side rendered. There is **no Node, no npm, no React build step** — please don't try to run `npm install` or `npm run dev`, it won't work.

## Project layout

```
sky_portal/        Project settings, root URLs, WSGI/ASGI entrypoints
accounts/          Registration, login, profile, password flows
core/              Dashboard, search, audit log, notifications, seed command
teams/             Teams, team members, dependencies, status history
organization/      Departments, team types, organisation structure view
messaging_app/     Inbox, sent, drafts, new message
scheduling/        Meeting scheduling and upcoming/weekly/monthly view
reports/           Summary reports + CSV/PDF export
analytics/         Charts (Chart.js)
templates/         All HTML templates, organised per app + a `shared/` folder
static/            Site-wide CSS
docs/              Coursework templates (group + individual)
```

## How to run it locally

These instructions work on macOS, Windows and the lab Linux machines. Run everything from the project root (`Group_Project_2026/`).

### 1. Clone and enter the folder

```bash
git clone <repo-url>
cd Group_Project_2026
```

### 2. Create a virtual environment and install dependencies

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 3. Apply migrations

```bash
.venv/bin/python manage.py migrate
```

> The repo ships with `db.sqlite3` already populated, so this step is usually a no-op. Running it is safe and confirms there are no schema changes pending.

### 4. (Optional) Re-seed demo data

If you want a clean database that already meets the brief's minimum-data rules (≥2 departments, ≥3 teams per department, ≥5 engineers per team), delete `db.sqlite3` and then run:

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_data
```

### 5. Create a superuser (for the Django admin)

```bash
.venv/bin/python manage.py createsuperuser
```

You'll be asked for a username, email and password. Use whatever you like for local testing.

### 6. Start the development server

```bash
.venv/bin/python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser. The first thing you'll see is the login page; sign up with a new account or log in with the superuser you just created.

To stop the server, press `Ctrl+C` in the terminal.

## Default test credentials

If you've used `createsuperuser` you can use those credentials. Otherwise, sign up at `/accounts/signup/` — the new account is auto-logged in and dropped on the dashboard.

> The submission `db.sqlite3` includes a working admin account; the username/password is listed in our coursework submission notes (kept out of the README so it doesn't leak into the repo).

## Common things you'll want to do

| What | Where to click | URL |
|---|---|---|
| Sign in | navbar | `/accounts/login/` |
| Register | login page → "Create account" | `/accounts/signup/` |
| Forgot password | login page → "Forgot password?" | `/accounts/password_reset/` |
| Change password | profile → "Change password" | `/accounts/password_change/` |
| Dashboard | navbar logo | `/` |
| Search teams / departments / managers | dashboard search box | `/` |
| Add a team | Teams → "Add team" | `/teams/new/` |
| Add a member to a team | team detail → "Add member" | `/teams/<id>/members/new/` |
| Add a dependency | team detail → "Add dependency" | `/teams/<id>/dependencies/new/` |
| Email a team | team detail → "Email team" | `/messages/new/?team=<id>` |
| Schedule a meeting | team detail → "Schedule meeting" | `/schedule/new/?team=<id>` |
| Inbox / Sent / Drafts | navbar → Messages | `/messages/` |
| Departments + types + relationships | navbar → Organisation | `/organization/structure/` |
| Reports + CSV/PDF export | navbar → Reports | `/reports/` |
| Charts | navbar → Charts | `/analytics/charts/` |
| Notifications | navbar bell | `/notifications/` |
| Audit log | navbar → Audit log | `/audit-log/` |
| Django admin | manual URL | `/admin/` |

## Note on the password reset email

We have not configured an SMTP server for the coursework submission. When you click "Forgot password?" the reset email is printed to the **console where `runserver` is running**, not sent over the network. Open the link from there to complete the reset. In a real deployment we'd plug in an SMTP backend or a transactional email provider.

## Running the tests

The repo has 15 Django unit tests that exercise the auth flow, the cache headers, the validation rules, the notification wiring and the report exports.

```bash
.venv/bin/python manage.py test
```

Expected output:

```
Ran 15 tests in ~2s
OK
```

## Resetting to a clean state

If anything gets weird (corrupted local database, stuck migration during development, etc.) you can always reset:

```bash
rm db.sqlite3
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_data
.venv/bin/python manage.py createsuperuser
```

You'll lose any local data but the seed command rebuilds enough rows to demo every page.

## Minimum data rules from the brief

The application enforces these at the model layer (so the rules apply through the UI, the Django admin and the shell):

- At least **2 departments** must exist at all times — `Department.delete()` blocks the last few deletions.
- Each department must keep **at least 3 teams** — `Team.delete()` blocks the deletion that would break this.
- A team can only be marked **Active** if it has **at least 5 engineers** — enforced in `Team.clean()` and `TeamMember.delete()`.

If you bypass them by editing `db.sqlite3` directly, the warnings on the dashboard ("compliance warnings") will tell you which rule is currently broken.

## Coursework submission notes

This repo is the **complete integrated project**. The submission also includes:

- `docs/cwk2_individual_template_Kapllani_W2064622.md` — Sefrid's individual template.
- `docs/cwk2_group_template_Kapllani_W2064622.md` — the group template (signed by every member).
- A short demo video — link is on page 1 of the group template.

If anything in this README doesn't work out of the box on the University's machines, please get in touch with the team before marking — we tested on macOS, Windows 11 and the lab Ubuntu image, but environments differ.
