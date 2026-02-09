# Unified Product Requirement Document (PRD): MyISP Skill Gap Analyzer

## 1. Executive Summary
**MyISP** is a web-based Skill Gap Analysis tool designed to identify, visualize, and bridge the gap between employee current proficiency and organizational requirements. It serves a 4-level organizational hierarchy, providing role-based visibility and actionable insights for up-skilling.

*   **Project Status:** Planned (Not Started).
*   **Core Function:** Track skill gaps, assign training plans, and monitor progress.
*   **Target Audience:** Employees, Managers, Delivery Leads (DL), Delivery Heads (DH), Group Delivery Leads (GDL).
*   **Delivery Constraints:** All phases must be delivered within 4 weeks (1 month).

## 2. Goals & Objectives
*   **Gap Visualization:** Clear comparison of Current vs. Expected proficiency levels.
*   **Actionable Planning:** Manager-driven creation, assignment, and tracking of up-skilling plans with milestones.
*   **Hierarchical Oversight:** Cascading visibility from GDL down to individual Managers.
*   **Data-Driven:** Support CSV imports for bulk updates, historical tracking, and nightly data refreshes.
*   **Dynamic Learning Plans:** Auto-update training plans based on skill proficiency changes in uploaded data.

## 3. User Personas & Hierarchy
The system enforces strict role-based data isolation and navigation.

| Role | Visibility Scope | Key Responsibilities |
| :--- | :--- | :--- |
| **Group Delivery Lead (GDL)** | Entire Enterprise (All DHs, DLs, Mgrs) | Strategic workforce planning, global trend analysis, enterprise-wide reporting. |
| **Delivery Head (DH)** | Their Org (All DLs, Mgrs, Teams) | Executive oversight, cross-team performance tracking, comparative trends. |
| **Delivery Lead (DL)** | Their Org (All Mgrs, Teams) | Org-level skill gap analysis, manager accountability, leaderboard tracking. |
| **Manager (Mgr)** | Direct Reports Only | Detailed employee review, assigning/cancelling training plans, feedback history, team gap analysis. |
| **Employee (IC/PM)** | Self Only | View profile, skill matrix, track training plan progress, view feedback. |
| **Admin** (Overlay) | System Config & Imports | Manage app settings, data imports, and delegate admin privileges to Managers+. |

## 4. Functional Requirements

### 4.1. General Interface & Behavior
*   **Role-Based Page Isolation Pattern:**
    *   Each role has its own complete set of pages (e.g., `manager-dashboard.html`, `manager-reports.html`).
    *   Pages must *never* link to pages from other roles. (e.g., `delivery-head-dashboard.html` can only link to `delivery-head-*.html`).
    *   Consistent naming convention: `{role}-{function}.html`.
*   **Smart Filter Bar Pattern:**
    *   Present on all management dashboards.
    *   Filters by Name, Manager, or Team via dropdowns or search input.
    *   Logic: Iterates through DOM elements with `data-*` attributes, hides non-matching rows, and auto-expands parent hierarchy sections to show matches.
*   **Expandable Dashboard Pattern:**
    *   Nested accordion views (GDL → DH → DL → Mgr → Employee).
    *   Visual hierarchy via color-coded headers (Dark Blue -> Medium Blue -> Light Blue).
    *   CSS-driven transitions: `max-height` toggle with `overflow: hidden` and icon rotation.
*   **Responsive Design:** Desktop-first approach.

### 4.2. Specific Role Features
*   **Admin (Overlay Role):**
    *   **Eligibility:** Must hold a role of Manager or above (Mgr, DL, DH, GDL).
    *   **Primary Admin:**
        *   Full access to **Settings** and **Data Import** pages.
        *   **Delegation:** Can search for and associate any Manager+ level user as a "Secondary Admin".
    *   **Secondary Admin:**
        *   Gains additional access to the **Data Import** page.
*   **Employee:**
    *   **Skill Matrix:** Visual grid of skills with "On-Target" (Green) or "Under-Skilled" (Red) status badges.
    *   **Up-Skill Plan:** Interactive cards showing Learning Need, Links, Milestones, and Deadlines. Supports deep linking to specific cards.
    *   **Feedback:** Timeline view of manager feedback and recognition.
    *   **Dual Alerts:** Distinct alerts for "Current Gaps" (Danger) and "Future Gaps" (Warning).
*   **Manager:**
    *   **Team Overview:** Flat table of direct reports with aggregated gap metrics.
    *   **Training Plan Management:**
        *   "Create" button generates plan based on gaps.
        *   Options: "Assign" (emails employee) or "Cancel".
        *   Set Milestones (e.g., Level 1 -> Level 2) and Deadlines.
    *   **Employee Details:** Drill-down view, feedback input (history timeline), plan review.
    *   **Data Import:** Drag-and-drop CSV upload with client-side preview (FileReader API) and row count.
*   **Leadership (DL, DH, GDL):**
    *   **Hierarchical Dashboards:** View subordinate levels with expandable sections.
    *   **Aggregated Metrics:** Total Skills, Gaps Identified, Completion Rates.
    *   **Reporting:** Leaderboards, comparative trends, problem skill identification.

### 4.3. Reporting Requirements
*   **Single-Page Mandate:** Aggregate, manager, and employee sections must be present on one printable page. No interactive drill-down required for the print view.
*   **Export Formats:**
    *   **PDF:** Must match the printable report layout exactly.
    *   **CSV:** Raw data rows.
*   **Metadata:** All exports must include Scope (Role + Filter), Date Range, Generated By (User ID), and Timestamp.
*   **Manager Level Report:** Per-employee skill gaps (severity, current vs target), plan status (Not Started/In Progress/Completed %), and time-series trends.
*   **Delivery Lead Level Report:** Aggregated skills gaps across managers, completion rates per manager, leaderboards, and trend views.
*   **Delivery Head Level Report:** Aggregated metrics across DLs, cross-lead comparisons, and top problem skills.
*   **GDL Level Report:** Enterprise rollups, comparative analytics across DHs, and executive summaries.

### 4.4. Data Model & Logic
*   **Source:** CSV-based (defaults to `sample_data.csv`). `sample_trainings.csv` for training resources.
*   **Key Fields:**
    *   **Hierarchy:** `GDLName`, `DHName`, `DLName`, `MgrName`.
    *   **Employee:** `Name`, `NBK` (ID), `Email`, `Role`, `FunctionName`, `PM/IC`.
    *   **Skill:** `SkillName`, `SkillType`, `EmpSkillCategory`, `User Proficiency`, `Expected Current Prof`, `GAP-Current`, `Expected Future Prof`, `GAP-Future`.
    *   **Training Resource:** `SkillName` (maps to Learning Need), `Tier` (New to Role, In Role Development, Mastery), `Resource URL 1`, `Resource URL 2`.
*   **Gap Logic:**
    *   **On-Target:** `User Proficiency` >= `Expected Current Prof`.
    *   **Under-Skilled:** `User Proficiency` < `Expected Current Prof`.
*   **Plan Automation:** System auto-completes plans if uploaded data shows proficiency target met.
*   **History:** Maintain state of assigned milestones/deadlines across data refreshes.
*   **Refresh Policy:** Nightly data refresh required. No on-demand refresh for reports.

## 5. Technical Architecture
*   **Backend:** Python (Flask).
    *   Dynamic routing based on role prefix (e.g., `/manager/*`).
    *   Jinja2 templating for server-side rendering.
    *   Pandas for efficient CSV processing and hierarchy generation.
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla).
    *   **Styles:** Global variables for enterprise palette (Deep Blues, Reds) in `styles.css`.
    *   **Interactivity:** Client-side filtering and accordion logic.
    *   **No Frameworks:** Lightweight, dependency-free implementation.
*   **Data Persistence:**
    *   **ORM:** SQLAlchemy (via Flask-SQLAlchemy) as the database abstraction layer. All database access MUST go through SQLAlchemy models — no raw SQL.
    *   **Local Development / Testing:** SQLite (`sqlite:///myisp.db`). Zero-config, file-based, no external dependencies.
    *   **Production:** PostgreSQL. The switch requires only changing the `DATABASE_URL` environment variable (e.g., `postgresql://user:pass@host/dbname`). No code changes needed.
    *   **Migrations:** Flask-Migrate (Alembic) for schema versioning. All schema changes must be captured as migration scripts.
    *   **Scope:** Database stores Training Plans, Milestones, Feedback, Settings, Import Logs, and Skill History. CSV remains the initial data source for bulk employee/skill imports.
    *   **Design Constraint:** Code must never use SQLite-specific features (e.g., no `PRAGMA`, no `AUTOINCREMENT` keyword). Use only SQLAlchemy-portable column types and queries.

## 6. Project Roadmap & Timelines (Total: 4 Weeks)

### Phase 1: Foundation & Prototypes (Duration: 1 Week)
*   **Deliverables:**
    *   Complete HTML/CSS/JS static prototypes for all 23 pages (Dashboards, Details, Reports, Import, Settings).
    *   Implementation of "Expandable Dashboard" and "Smart Filter" patterns.
    *   Strict Role-based page isolation structure.
*   **Key Activities:** UI/UX design, frontend coding, mock data binding.

### Phase 2: Backend Core & Data Processing (Duration: 1 Week)
*   **Deliverables:**
    *   Flask application setup with Jinja2 templates.
    *   CSV parsing engine (Pandas) to build nested hierarchy objects.
    *   Role-based routing logic.
*   **Key Activities:** Converting static HTML to templates, implementing gap calculation logic, server-side data loading.

### Phase 3: Persistence, Logic & Workflows (Duration: 1 Week)
*   **Deliverables:**
    *   Database schema for Employees, Skills, Training Plans, and Feedback.
    *   "Assign/Cancel" workflow implementation for Managers.
    *   Milestone tracking and auto-completion logic based on new data uploads.
    *   Data Import feature (parsing + validation).
*   **Key Activities:** DB integration, API endpoints for plan management, state management implementation.

### Phase 4: Analytics, Reporting & Final Polish (Duration: 1 Week)
*   **Deliverables:**
    *   Aggregated reporting views (Leaderboards, Trends) for Leadership.
    *   Export functionality (PDF/CSV) with metadata.
    *   Final UI polish and cross-browser testing.
    *   Nightly data refresh scheduler.
*   **Key Activities:** Complex query optimization, Chart.js integration (if needed), rigorous testing.

## 7. Success Metrics
*   **Delivery:** All 4 phases completed within the 1-month window.
*   **Performance:** Dashboard load time < 2 seconds for GDL view (full hierarchy).
*   **Usability:** Zero cross-role link errors.
*   **Accuracy:** 100% accuracy in gap identification and plan auto-completion logic.
