from flask import Blueprint, render_template, request
from app.utils import get_employees_by_manager, get_employee_summary, get_employee_details_context

bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/dashboard')
def dashboard():
    """Manager dashboard showing direct reports."""
    # For demo, use Harvey Specter as the logged-in manager
    manager_name = request.args.get('manager', 'Harvey Specter')

    # Get employees under this manager
    employees_list = get_employees_by_manager(manager_name)
    employees_summary = get_employee_summary(employees_list)

    # Apply filters if any
    search = request.args.get('search', '').lower()
    employee_filter = request.args.get('employee', '')

    if search:
        employees_summary = [e for e in employees_summary if search in e['name'].lower() or search in e['nbk'].lower()]
    if employee_filter:
        employees_summary = [e for e in employees_summary if e['nbk'] == employee_filter]

    # For the filter dropdown, we need the full list of employees under this manager
    # We can use the original employees_summary before filtering, or re-fetch. 
    # Original code passed 'all_employees' which was the full summary.
    all_employees_summary = get_employee_summary(employees_list)

    return render_template('manager/dashboard.html',
                         manager_name=manager_name,
                         employees=employees_summary,
                         all_employees=all_employees_summary)

@bp.route('/employee/<nbk>')
def employee_details(nbk):
    """Employee details view for manager."""
    context = get_employee_details_context(nbk)
    if not context:
        return render_template('errors/404.html'), 404

    return render_template('manager/employee_details.html',
                         manager_name='Harvey Specter',
                         **context)

@bp.route('/reports')
def reports():
    """Manager reports view."""
    manager_name = request.args.get('manager', 'Harvey Specter')
    employees_list = get_employees_by_manager(manager_name)
    employees_summary = get_employee_summary(employees_list)

    # Calculate gap statistics
    total_skills = sum(e['total_skills'] for e in employees_summary)
    current_gaps = sum(e['current_gaps'] for e in employees_summary)

    return render_template('manager/reports.html',
                         manager_name=manager_name,
                         employees=employees_summary,
                         total_skills=total_skills,
                         current_gaps=current_gaps)

@bp.route('/import-data')
def import_data():
    """Manager data import view."""
    return render_template('manager/import_data.html')

@bp.route('/settings')
def settings():
    """Manager settings view."""
    manager_name = request.args.get('manager', 'Harvey Specter')
    return render_template('manager/settings.html', manager_name=manager_name)
