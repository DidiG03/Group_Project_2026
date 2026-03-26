# Sky Engineering Teams Portal

This is our group coursework project for `5COSC021W Software Development Group Project`.

The application replaces a shared spreadsheet with a Django web portal where users can:

- register and login,
- search teams, departments, and managers,
- view team details (mission, members, contact, repositories),
- view upstream/downstream dependencies,
- use messaging and meeting scheduling pages,
- export reports in CSV (Excel-compatible) and PDF format,
- view charts for departments and managers,
- view in-app notifications and status updates,
- manage records through Django admin,
- keep an audit trail of updates.

## Tech Stack

- Python
- Django
- SQLite
- Bootstrap

## Project Structure

- `accounts` - registration, login, profile, password flows
- `core` - dashboard, search, audit logs, seed command
- `teams` - teams, team members, dependencies
- `organization` - departments, team type, structure view
- `messaging_app` - inbox/sent/draft/new message
- `scheduling` - meeting scheduling and upcoming views
- `reports` - summary reports and exports
- `analytics` - charts and visualisation pages

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. Apply migrations:

   ```bash
   .venv/bin/python manage.py migrate
   ```

3. Seed sample coursework data:

   ```bash
   .venv/bin/python manage.py seed_data
   ```

4. Create an admin user:

   ```bash
   .venv/bin/python manage.py createsuperuser
   ```

5. Start the server:

   ```bash
   .venv/bin/python manage.py runserver
   ```

Then open `http://127.0.0.1:8000/`.

## Test

```bash
.venv/bin/python manage.py test
```

## Minimum Data Rules (Coursework)

The seed command creates data aligned with the brief:

- at least 2 departments,
- at least 3 teams per department,
- at least 5 engineers per team.

## Notes for Submission

- Include the full Django project and SQLite database.
- Include group and individual templates.
- Include testing evidence and version control evidence.
- Include video demo link (5-10 minutes).
