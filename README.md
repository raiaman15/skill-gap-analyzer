# MyISP Skill Gap Analyzer

**MyISP** is a web-based tool for tracking and managing employee skill development across a 4-level organizational hierarchy. It visualizes skill gaps and facilitates manager-driven up-skilling plans.

For detailed functional requirements, user personas, architecture, and timelines, please refer to [PRD.md](PRD.md).

## Project Structure

```
skill-gap-analyzer/
├── README.md                # Setup and installation guide
├── PRD.md                   # Comprehensive Product Requirement Document
├── sample.csv               # Sample data with organizational hierarchy
├── app.py                   # Flask application entry point
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── static/                  # Static assets (CSS, JS)
└── templates/               # Jinja2 HTML templates
```

## Getting Started

### Prerequisites

*   **Python 3.8+**
*   **pip** (Python package manager)
*   Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd skill-gap-analyzer
    ```

2.  **Create and activate a virtual environment:**
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open your browser and navigate to `http://localhost:8080/`. You will see a landing page to select a role for demonstration purposes.

    **Direct Role Links (for testing with sample data):**
    *   **Employee:** `http://localhost:8080/employee/dashboard?nbk=mr002`
    *   **Manager:** `http://localhost:8080/manager/dashboard?manager=Harvey%20Specter`
    *   **Delivery Lead:** `http://localhost:8080/delivery-lead/dashboard?dl=Robert%20Zane`
    *   **Delivery Head:** `http://localhost:8080/delivery-head/dashboard?dh=Jessica%20Pearson`
    *   **Group Delivery Lead:** `http://localhost:8080/group-delivery-lead/dashboard?gdl=Daniel%20Hardman`

## Customization

*   **Data Source:** Replace `sample.csv` with your organization's data. Ensure the column headers match the specifications in the "Data Model" section of `PRD.md`.
*   **Branding:** Update `static/css/styles.css` for color palette changes and `templates/base.html` for logo/footer text.
*   **Configuration:** Set `debug=False` in `app.py` for production environments.

## Technologies

*   **Backend:** Python (Flask), Pandas
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2
*   **Data:** CSV (Flat file storage)