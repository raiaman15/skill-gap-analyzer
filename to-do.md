# MyISP Skill Gap Analyzer — Master To-Do List

> Generated from PRD-vs-Implementation audit (Feb 2026).
> Items are grouped by phase, then by priority within each phase.
> Each task includes the specific steps required to complete it.

---

## Legend

- **[P0]** — Blocker / Breaks core functionality
- **[P1]** — High priority / PRD-required feature
- **[P2]** — Medium priority / Quality & polish
- **[P3]** — Low priority / Nice-to-have improvement

---

## Phase 0: Pre-Work — Cleanup & Foundation Fixes

These must be done before any new feature work so the codebase is in a clean state.

### 0.1 [P0] Remove orphaned `public/` directory
The 25 static HTML prototypes are no longer served by Flask. They are dead code.
- [x] Verify no Flask route references `public/`
- [x] Delete `public/` directory entirely (or move to an `archive/` folder if you want to keep history)
- [x] Remove empty `public/assets/` and `public/js/` directories

### 0.2 [P0] Fix `sample.csv` naming inconsistency
PRD §4.4 says "defaults to `sample.csv`" but the file is `sample_data.csv`.
- [ ] **Option A:** Rename `sample_data.csv` → `sample.csv` and update `app.py:16`
- [x] **Option B:** Update PRD §4.4 to say `sample_data.csv` *(chosen — PRD updated)*
- [x] Whichever option: ensure the reference is consistent everywhere

### 0.3 [P1] Remove unused `jsonify` import
- [x] Remove `jsonify` from `app.py:6` import line (will re-add when API endpoints are built)

### 0.4 [P2] Move inline CSS to stylesheet
~370 lines of CSS are embedded in templates via `{% block extra_css %}`.
- [x] Extract CSS from `delivery_lead/dashboard.html` (lines 17–190) into `styles.css`
- [x] Extract CSS from `employee/upskill_plan.html` (lines 16–184) into `styles.css`
- [x] Extract CSS from `delivery_head/dashboard.html` into `styles.css`
- [x] Extract CSS from `group_delivery_lead/dashboard.html` into `styles.css`
- [x] Replace all excessive `style="..."` inline attributes with CSS classes
- [x] Audit every template for remaining inline styles and consolidate

### 0.5 [P2] Add proper error pages
- [x] Create `templates/errors/404.html` extending `base.html`
- [x] Create `templates/errors/500.html` extending `base.html`
- [x] Register Flask error handlers in `app.py` for 404 and 500
- [x] Replace raw string returns (e.g., `app.py:111`) with `render_template('errors/404.html')`

### 0.6 [P2] Add responsive CSS
PRD §4.1 specifies "Desktop-first responsive design". No `@media` queries exist.
- [x] Add `@media` breakpoints to `styles.css` for tablet (≤1024px) and mobile (≤768px)
- [x] Make `.kpi-row` stack vertically on small screens
- [x] Make `.filter-grid` single-column on small screens
- [x] Test all dashboards at each breakpoint

---

## Phase 1: Database & ORM Setup (Phase 3 of PRD)

### 1.1 [P0] Install and configure SQLAlchemy ORM
Use SQLAlchemy so the database engine can be swapped between SQLite (local) and PostgreSQL (production) by changing a single connection string.
- [ ] Add `Flask-SQLAlchemy>=3.1.0` and `Flask-Migrate>=4.0.0` to `requirements.txt`
- [ ] Create `config.py` with:
  ```python
  import os
  class Config:
      SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///myisp.db')
      SQLALCHEMY_TRACK_MODIFICATIONS = False
  ```
- [ ] Update `app.py` to use `app.config.from_object(Config)`
- [ ] Initialize `db = SQLAlchemy(app)` and `migrate = Migrate(app, db)`
- [ ] Remove hardcoded `SECRET_KEY` from `app.py:11`
- [ ] Add `*.db` and `*.sqlite` to `.gitignore` (already done)
- [ ] Create `env.example` file documenting required environment variables
- [ ] Verify the app starts with SQLite by default (`sqlite:///myisp.db`)
- [ ] Verify that changing `DATABASE_URL` to a PostgreSQL connection string works

### 1.2 [P0] Define database models
Create `models.py` with the following ORM models:
- [ ] **Employee** model:
  - `nbk` (PK, String) — unique employee ID
  - `name` (String, not null)
  - `email` (String)
  - `role` (String) — job title
  - `function_name` (String)
  - `pm_ic` (String) — "PM" or "IC"
  - `manager_name` (String, FK ref)
  - `dl_name` (String)
  - `dh_name` (String)
  - `gdl_name` (String)
- [ ] **Skill** model:
  - `id` (PK, Integer, auto-increment)
  - `employee_nbk` (FK → Employee.nbk)
  - `skill_name` (String)
  - `skill_type` (String) — Technical, Soft Skill, etc.
  - `emp_skill_category` (String) — Primary, Core, etc.
  - `user_proficiency` (String) — Level 1–4
  - `expected_current_prof` (String)
  - `gap_current` (String) — computed or imported
  - `expected_future_prof` (String)
  - `gap_future` (String)
  - `last_updated` (DateTime)
- [ ] **TrainingPlan** model:
  - `id` (PK, Integer, auto-increment)
  - `employee_nbk` (FK → Employee.nbk)
  - `skill_name` (String)
  - `status` (String) — "Not Started", "In Progress", "Completed", "Cancelled"
  - `assigned_by` (String) — manager name
  - `assigned_date` (DateTime)
  - `target_proficiency` (String)
  - `deadline` (Date)
  - `completion_date` (DateTime, nullable)
  - `notes` (Text, nullable)
- [ ] **Milestone** model:
  - `id` (PK, Integer, auto-increment)
  - `training_plan_id` (FK → TrainingPlan.id)
  - `title` (String) — e.g., "Level 1 → Level 2"
  - `target_level` (String)
  - `deadline` (Date)
  - `completed` (Boolean, default False)
  - `completed_date` (DateTime, nullable)
- [ ] **Feedback** model:
  - `id` (PK, Integer, auto-increment)
  - `employee_nbk` (FK → Employee.nbk)
  - `given_by` (String) — manager name
  - `feedback_type` (String) — "Recognition", "Improvement", "General"
  - `content` (Text)
  - `created_at` (DateTime, default utcnow)
- [ ] **DataImportLog** model:
  - `id` (PK, Integer, auto-increment)
  - `imported_by` (String)
  - `filename` (String)
  - `row_count` (Integer)
  - `status` (String) — "Success", "Failed", "Partial"
  - `imported_at` (DateTime, default utcnow)
  - `error_message` (Text, nullable)
- [ ] **Setting** model:
  - `id` (PK, Integer, auto-increment)
  - `user_name` (String)
  - `role` (String)
  - `email_notifications` (Boolean, default True)
  - `updated_at` (DateTime)

### 1.3 [P0] Create initial migration and seed script
- [ ] Run `flask db init` to create migrations directory
- [ ] Run `flask db migrate -m "initial schema"` to generate migration
- [ ] Run `flask db upgrade` to create tables
- [ ] Create `seed.py` script that:
  - Reads `sample_data.csv` via Pandas
  - Populates Employee and Skill tables
  - Reads `sample_trainings.csv` and stores training resource links
- [ ] Run seed script and verify data is in SQLite

### 1.4 [P1] Create a TrainingResource model and load `sample_trainings.csv`
The file exists but is never used.
- [ ] **TrainingResource** model:
  - `id` (PK, Integer, auto-increment)
  - `skill_name` (String)
  - `tier` (String) — "New to Role", "In Role Development", "Mastery"
  - `resource_url_1` (String)
  - `resource_url_2` (String)
- [ ] Load data from `sample_trainings.csv` in the seed script
- [ ] Update upskill plan template to show real training links instead of "Training module for {skill_name}"

### 1.5 [P1] Refactor `app.py` to use ORM queries instead of Pandas
- [ ] Replace `load_data()` and global `df_data` with SQLAlchemy queries
- [ ] Replace `get_employees_by_manager()` with `Employee.query.filter_by(manager_name=...)`
- [ ] Replace `get_managers_by_dl()` with distinct query on Employee table
- [ ] Replace `get_dls_by_dh()` with distinct query on Employee table
- [ ] Replace `get_dhs_by_gdl()` with distinct query on Employee table
- [ ] Replace `get_employee_summary()` with a query + aggregation method on the model
- [ ] Keep Pandas as a dependency only for CSV import processing
- [ ] Fix the DL dashboard bug: `app.py:179` incorrectly uses first employee's NBK/Role for the manager card

---

## Phase 2: Server-Side Gap Calculation & Validation

### 2.1 [P0] Implement server-side gap calculation logic
PRD §4.4 specifies gap logic but the app just reads pre-computed CSV columns.
- [ ] Create a utility function `calculate_gap(user_prof, expected_prof)`:
  - Parse proficiency strings (e.g., "Level 2: Practitioner") to numeric values
  - Return "On-Target" if user >= expected, "Under-Skilled" otherwise
- [ ] Apply this function during CSV import instead of trusting CSV `GAP-Current`/`GAP-Future` columns
- [ ] Add validation: reject rows where proficiency values are missing or malformed
- [ ] Store computed gap values in the Skill model

### 2.2 [P1] Add CSV data validation on import
- [ ] Validate required columns exist in uploaded CSV
- [ ] Validate data types and value ranges (proficiency levels 1–4)
- [ ] Return detailed error messages for invalid rows
- [ ] Reject files exceeding a configurable row limit

---

## Phase 3: POST Endpoints & Workflows

### 3.1 [P0] Add CSRF protection
- [ ] Add `Flask-WTF>=1.2.0` to `requirements.txt`
- [ ] Initialize `CSRFProtect(app)` in `app.py`
- [ ] Add `{{ csrf_token() }}` or `<input type="hidden" name="csrf_token" ...>` to all forms
- [ ] Add CSRF token to AJAX requests via meta tag

### 3.2 [P0] Implement CSV import POST endpoint
- [ ] Create `POST /manager/import-data` route
- [ ] Accept multipart file upload
- [ ] Parse CSV with Pandas, validate structure and data
- [ ] Upsert Employee and Skill records in database
- [ ] Recompute gap values server-side
- [ ] Log import in DataImportLog table
- [ ] Return success/error response with row count and any validation errors
- [ ] Wire up the "Process Import" button in all import templates

### 3.3 [P0] Implement Training Plan Assign/Cancel workflow
PRD §4.2: Manager creates, assigns, or cancels plans.
- [ ] Create `POST /manager/employee/<nbk>/plan/create` — auto-generates plan from current gaps
- [ ] Create `POST /manager/employee/<nbk>/plan/<plan_id>/assign` — sets status to "In Progress"
- [ ] Create `POST /manager/employee/<nbk>/plan/<plan_id>/cancel` — sets status to "Cancelled"
- [ ] Enable the currently disabled "Assign Plan" and "View Plan" buttons
- [ ] Add milestone creation form: target level + deadline
- [ ] Add milestone display in employee details view
- [ ] Implement plan auto-completion: when new CSV data shows proficiency meets target, auto-set status to "Completed"

### 3.4 [P0] Implement Feedback submission
PRD §4.2: Manager feedback input with history timeline.
- [ ] Create `POST /manager/employee/<nbk>/feedback` route
- [ ] Accept: feedback_type, content
- [ ] Store in Feedback table with `given_by` = current manager
- [ ] Update manager employee_details template to submit form via POST
- [ ] Update employee feedback template to display real feedback from database
- [ ] Show feedback as a timeline view (newest first) with dates and manager names
- [ ] Enable the "Load More History" button with pagination

### 3.5 [P1] Implement Settings save
- [ ] Create `POST /manager/settings` route
- [ ] Create `POST /delivery-lead/settings` route
- [ ] Create `POST /delivery-head/settings` route
- [ ] Create `POST /group-delivery-lead/settings` route
- [ ] Save email notification toggle to Setting table
- [ ] Wire up the "Save Settings" button in all settings templates
- [ ] Show success/error flash message after save

### 3.6 [P1] Add input validation and sanitization
- [ ] Validate all query parameters (`?manager=`, `?nbk=`, `?dl=`, `?dh=`, `?gdl=`)
- [ ] Return 400 for invalid/empty parameters instead of showing empty pages
- [ ] Sanitize all user inputs before database writes
- [ ] Add rate limiting on POST endpoints

---

## Phase 4: UI Fixes & PRD Compliance

### 4.1 [P0] Add Employee Dual Alerts
PRD §4.2 requires two distinct alerts. Currently only one (Danger for current gaps) exists.
- [ ] Add a **Warning alert** for "Future Gaps" to `employee/upskill_plan.html`
  - Yellow/amber styling with `alert-warning` class
  - Text: "You have X future skill gaps to prepare for"
- [ ] Keep existing **Danger alert** for "Current Gaps"
- [ ] Show both alerts only when relevant counts > 0
- [ ] Also add future gap skills to the upskill plan cards (currently only shows current gaps)

### 4.2 [P1] Fix proficiency meter visualization
The meter at `upskill_plan.html:222-226` displays full strings like "Level 2: Practitioner" in tiny circles.
- [ ] Parse proficiency strings to extract numeric level (1, 2, 3, 4)
- [ ] Pass numeric values from `app.py` to template
- [ ] Render all 4 steps always, highlight "current" and "target" with correct positioning
- [ ] Add proper labels below each step ("Novice", "Practitioner", "Expert", "Master")

### 4.3 [P1] Implement deep linking for upskill plan cards
PRD §4.2: "Supports deep linking to specific cards."
- [ ] Add `id` attributes to each skill card wrapper (e.g., `id="skill-{skill_name_slug}"`)
- [ ] Add URL hash support: if `#skill-name` is in URL, auto-expand that card
- [ ] Add JavaScript to scroll to and expand the targeted card on page load
- [ ] Update "Start Training" links on employee dashboard to include `#skill-{slug}` hash

### 4.4 [P1] Fix color-coded hierarchy headers
PRD §4.1: "Dark Blue → Medium Blue → Light Blue" cascade.
- [ ] Define 3 header gradient levels in `styles.css`:
  - Level 1 (DH section in GDL view): Dark blue gradient (`#001871` → `#003087`)
  - Level 2 (DL section): Medium blue gradient (`#1a5490` → `#2a7ac0`)
  - Level 3 (Manager section): Light blue gradient (`#e8f4f8` → `#d0e8f0`)
- [ ] Apply consistently across `group_delivery_lead/dashboard.html`, `delivery_head/dashboard.html`, and `delivery_lead/dashboard.html`

### 4.5 [P1] Fix accordion transition consistency
PRD §4.1: Use `max-height` toggle everywhere.
- [ ] Update `employee/upskill_plan.html` to use `max-height` + `overflow: hidden` transition instead of `display: none/block`
- [ ] Add icon rotation animation to all expand/collapse interactions
- [ ] Ensure consistent transition timing across all accordion components

### 4.6 [P2] Fix template cross-role inheritance
PRD §4.1: Strict role-based page isolation.
- [ ] Copy shared logic from `manager/import_data.html` into each role's own template (DL, DH, GDL) so they are self-contained
- [ ] Copy shared logic from `delivery_lead/employee_details.html` into DH and GDL versions
- [ ] Copy shared logic from `delivery_lead/settings.html` into DH version
- [ ] Each role's template directory should be fully self-contained
- [ ] Alternatively: extract shared components into a `_partials/` directory and include them (acceptable since partials aren't full pages)

---

## Phase 5: Reporting & Analytics (Phase 4 of PRD)

### 5.1 [P0] Fix GDL reports — currently passes no data
- [ ] Update `app.py:345-347` (`group_delivery_lead_reports()`) to:
  - Query all data under the GDL
  - Compute: total DHs, total DLs, total managers, total employees, total skills, total gaps
  - Aggregate gap percentages per DH
- [ ] Pass computed data to template

### 5.2 [P0] Implement Manager-level reports (PRD §4.3)
- [ ] Per-employee skill gaps with severity (count + percentage)
- [ ] Current vs target proficiency table
- [ ] Plan status breakdown: Not Started / In Progress / Completed %
- [ ] Replace `[Interactive Chart Component Placeholder]` with Chart.js bar/pie chart
- [ ] Add Chart.js to project (via CDN or local file in `static/js/`)

### 5.3 [P0] Implement Delivery Lead reports (PRD §4.3)
- [ ] Aggregated skill gaps across all managers under the DL
- [ ] Completion rates per manager (table + chart)
- [ ] Leaderboard: rank managers by gap closure rate
- [ ] Trend view placeholder (requires historical data from Phase 6)

### 5.4 [P1] Implement Delivery Head reports (PRD §4.3)
- [ ] Aggregated metrics across all DLs under the DH
- [ ] Cross-lead comparisons (table + chart)
- [ ] Top 5 problem skills (most gaps across the org)
- [ ] Currently only shows 1 KPI card — expand to full report

### 5.5 [P1] Implement GDL reports (PRD §4.3)
- [ ] Enterprise rollups across all DHs
- [ ] Comparative analytics: DH-level performance comparison
- [ ] Executive summary section with key metrics

### 5.6 [P1] Implement Export — CSV
- [ ] Create `GET /manager/reports/export/csv` route
- [ ] Create equivalent routes for DL, DH, GDL
- [ ] Generate CSV with: employee data, gap data, plan status
- [ ] Include metadata header: Scope, Date Range, Generated By, Timestamp (PRD §4.3)
- [ ] Wire up "Export to CSV" buttons in all report templates

### 5.7 [P1] Implement Export — PDF
- [ ] Add `weasyprint` or `xhtml2pdf` to `requirements.txt`
- [ ] Create `GET /manager/reports/export/pdf` route
- [ ] Create equivalent routes for DL, DH, GDL
- [ ] Render a print-optimized template with all sections on one page (PRD §4.3 single-page mandate)
- [ ] Include metadata: Scope, Date Range, Generated By, Timestamp
- [ ] Wire up "Export to PDF" buttons in all report templates

### 5.8 [P2] Implement Leaderboards
- [ ] Manager leaderboard on DL reports: rank by fewest gaps, highest completion rate
- [ ] DL leaderboard on DH reports: rank by aggregate performance
- [ ] Style as a ranked list with position badges (1st, 2nd, 3rd)

---

## Phase 6: Historical Tracking & Automation

### 6.1 [P1] Implement historical data snapshots
- [ ] Create **SkillHistory** model:
  - `id`, `employee_nbk`, `skill_name`, `user_proficiency`, `gap_current`, `snapshot_date`
- [ ] On each CSV import, snapshot all current Skill records into SkillHistory before updating
- [ ] Query SkillHistory for time-series data on reports

### 6.2 [P1] Implement plan auto-completion logic
PRD §4.4: "System auto-completes plans if uploaded data shows proficiency target met."
- [ ] After each CSV import, for each active TrainingPlan:
  - Check if the employee's new proficiency for that skill meets or exceeds the plan's target
  - If yes: set `status = "Completed"`, `completion_date = now()`
  - Mark all associated milestones as completed
- [ ] Log auto-completions for audit trail

### 6.3 [P1] Implement time-series trend charts
- [ ] Query SkillHistory for gap counts over time per employee/team
- [ ] Render line charts using Chart.js on report pages
- [ ] Show trends for: gap count over time, completion rate over time

### 6.4 [P2] Implement nightly data refresh scheduler
PRD §4.4: "Nightly data refresh required."
- [ ] Add `APScheduler` or `celery-beat` to `requirements.txt`
- [ ] Create a scheduled job that:
  - Reads a configured CSV source path
  - Runs the same import logic as manual CSV upload
  - Logs results in DataImportLog
- [ ] Configure schedule: daily at a configurable time (default 2:00 AM)
- [ ] Add scheduler config to `config.py`

---

## Phase 7: Security & Production Readiness

### 7.1 [P0] Environment-based configuration
- [ ] Load `SECRET_KEY` from environment variable (already in config.py from 1.1)
- [ ] Load `DATABASE_URL` from environment variable
- [ ] Remove `debug=True` from `app.py:435` — use `FLASK_DEBUG` env var instead
- [ ] Create `.env.example` documenting all environment variables

### 7.2 [P1] Add error handling on CSV load
- [ ] Wrap CSV reading in try/except in `seed.py` and import routes
- [ ] Show meaningful error if file is missing, empty, or malformed
- [ ] Log errors to application logger

### 7.3 [P2] Add request logging
- [ ] Configure Flask logger with structured output
- [ ] Log all POST requests with user context
- [ ] Log all errors with stack traces

---

## Phase 8: Final Polish & PRD Compliance Verification

### 8.1 [P1] Naming convention audit
PRD §4.1: Consistent `{role}-{function}` naming.
- [ ] Decide on one convention for template files (hyphens vs underscores)
- [ ] Rename templates if needed for consistency
- [ ] Update all `url_for()` references accordingly

### 8.2 [P1] Performance verification
PRD §7: "Dashboard load time < 2 seconds for GDL view."
- [ ] Profile GDL dashboard with full hierarchy
- [ ] Optimize ORM queries (eager loading, avoiding N+1)
- [ ] Add database indexes on `manager_name`, `dl_name`, `dh_name`, `gdl_name`
- [ ] Test with larger dataset (100+ employees)

### 8.3 [P1] Cross-role link audit
PRD §7: "Zero cross-role link errors."
- [ ] Audit every `<a href>` and `url_for()` in every template
- [ ] Ensure no template links to a route outside its role prefix
- [ ] Write a simple test script that parses all templates and flags violations

### 8.4 [P2] Cross-browser testing
- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] Fix any CSS compatibility issues
- [ ] Verify all JavaScript works across browsers

### 8.5 [P2] DRY up duplicated logic
- [ ] Employee dashboard (`app.py:363-395`) manually recalculates gaps that `get_employee_summary()` already computes — consolidate
- [ ] Extract common route patterns (e.g., employee-details delegation) into shared helpers

---

## Summary: Completion Tracker

| Phase | Description | Priority Tasks | Status |
|-------|-------------|---------------|--------|
| 0 | Cleanup & Foundation Fixes | 6 tasks | Not Started |
| 1 | Database & ORM Setup | 5 tasks | Not Started |
| 2 | Gap Calculation & Validation | 2 tasks | Not Started |
| 3 | POST Endpoints & Workflows | 6 tasks | Not Started |
| 4 | UI Fixes & PRD Compliance | 6 tasks | Not Started |
| 5 | Reporting & Analytics | 8 tasks | Not Started |
| 6 | Historical Tracking & Automation | 4 tasks | Not Started |
| 7 | Security & Production Readiness | 3 tasks | Not Started |
| 8 | Final Polish & Verification | 5 tasks | Not Started |
| **Total** | | **45 tasks** | |
