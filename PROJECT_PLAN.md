# Project Plan: Skill Gap Analyzer

## 1. Executive Summary
The **Skill Gap Analyzer** is a web-based application designed to help organizations identify and bridge the gap between employees' current skill sets and required proficiency levels. The system serves two primary roles: **Employees**, who track their development, and **Managers**, who oversee team competency and planning.

## 2. Goals & Objectives
- **Visualize Proficiency:** Clear comparison between current and expected skill levels.
- **Actionable Insights:** Generate up-skilling plans for identified gaps.
- **Management Oversight:** Provide managers with a high-level view of team health and individual progress.

## 3. Target Audience
- **Employees (IC/PM):** View personal skill gaps, career path, and training plans.
- **Managers:** View team skill status, import data, and generate reports.

## 4. UI/UX Strategy
- **Visual Style:** Corporate, professional aesthetic inspired by **Internal Enterprise Tooling**.
  - **Color Palette:** Deep Blues (Trust/Corporate), Reds (Alerts/Gaps), White/Light Grey backgrounds.
  - **Typography:** Clean sans-serif fonts (e.g., Arial, Roboto, Open Sans).
  - **Components:** High-density data tables, clear status indicators (badges), standard form inputs, top navigation bar.

## 5. Data Model (from `sample.csv`)
The application will strictly adhere to the following data schema. 
*Note: `SkillType` and `EmpSkillCategory` columns exist in the source data but are currently hidden in the UI to streamline the user experience.*

| Column Header | Description | Data Type / Example |
| :--- | :--- | :--- |
| **Name** | Employee Full Name | String (e.g., "Harvey Specter") |
| **NBK** | Unique Employee ID | String (e.g., "hs001") |
| **Email** | Contact Email | String |
| **GDLName** | Global Division | String (e.g., "Pearson Hardman") |
| **DHName** | Department Head / Location | String (e.g., "NYC Office") |
| **DLName** | Department Level | String (e.g., "Legal Dept") |
| **MgrName** | Direct Manager's Name | String |
| **FunctionName** | Job Function | String (e.g., "Corporate Litigation") |
| **Role** | Job Title | String (e.g., "Senior Partner") |
| **PM/IC** | People Manager or Individual Contributor | Enum (PM, IC) |
| **SkillName** | Name of the Skill | String (e.g., "Negotiation") |
| **SkillType** | Classification | Enum (Soft Skill, Technical, etc.) |
| **EmpSkillCategory**| Importance Category | Enum (Primary, Secondary, Core) |
| **User Proficiency** | Current Self/Assessed Level | String (e.g., "Level 1: Proficient") |
| **Expected Current Prof** | Target Level (Now) | String |
| **GAP-Current** | Current Readiness Indicator | Enum (Under-Skilled, On-Target) |
| **Expected Future Prof** | Target Level (Future) | String |
| **GAP-Future** | Future Status Indicator | Enum (Under-Skilled, Not Selected) |

## 6. Development Phases

### Phase 1: Frontend Prototypes (HTML/CSS/JS)
**Objective:** Create static, high-fidelity mockups of key user journeys. No real backend; mock data and client-side logic used for visualization.

**Deliverables:**

1.  **Employee Dashboard** (`employee-dashboard.html`)
    *   **Consolidated Profile:** User details (Role, Manager, Contact) merged into the main dashboard view.
    *   **Summary Cards:** Total Skills, Gaps Identified (aligned with CSV data).
    *   **Competency Matrix:** List of skills with visual readiness status.
    *   **Status Indicators:** Color-coded badges for *Current Readiness*.

2.  **Manager Dashboard** (`manager-dashboard.html`)
    *   **Team Overview Table:** List of direct reports (filtered by `MgrName`) with search functionality.
    *   **Aggregated Metrics:** Direct Reports count, Team Skill Gaps.
    *   **Drill-down:** Ability to click an employee to see their details (linking to `manager-employee-details.html`).

3.  **Employee Up-Skill Plan Page** (`employee-upskill-plan.html`)
    *   **Card Grid Layout:** Skills are presented as individual cards, expandable to show details.
    *   **Dual Alerts:** Separate "Danger" (Current Gaps) and "Warning" (Future Gaps) alerts for immediate clarity.
    *   **Deep Linking:** Supports query parameters to automatically expand specific skill cards from the dashboard.
    *   **Detail View:** Focus on a single selected skill (e.g., "Negotiation").
    *   **Gap Analysis:** Visual representation of Level 1 vs Level 2.
    *   **Action Plan:** Placeholder for "Recommended Training Modules".

4.  **Manager Data Import** (`manager-import-data.html`)
    *   **File Upload Area:** Drag-and-drop zone with large folder icon support.
    *   **Real-time Preview:** Client-side CSV parsing showing all columns and up to 1000 rows.
    *   **Row Count:** Summary display of total records found.

5.  **Employee Details Page** (`manager-employee-details.html`)
    *   **Drill-Down View:** Detailed view for managers to inspect a specific employee's skill matrix.
    *   **Manager Feedback:** Integrated input section for adding new feedback and a history timeline of past interactions.
    *   **Actions:** Links to assign or view upskilling plans.

6.  **Navigation & Support Pages**
    *   **Manager Feedback** (`employee-feedback.html`): Dedicated timeline view for employees to see historical feedback and recognition.
    *   **Reports** (`manager-reports.html`): Skill Distribution Analysis (Charts) and Detailed Report (Skills with Gaps).
    *   **Settings** (`manager-settings.html`): Email notification preferences (On/Off).

### Phase 2: Backend Functionality (Future Scope)
**Objective:** Implement persistent storage, authentication, and business logic.
*   Database setup (SQL/NoSQL).
*   API Development (REST/GraphQL).
*   Authentication (SSO/JWT).
*   Server-side CSV parsing and data validation.