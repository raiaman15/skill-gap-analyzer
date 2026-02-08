from flask import render_template, request
from app.delivery_lead import bp
from app.utils import get_managers_by_dl, get_employees_by_manager, get_employee_summary, get_employee_details_context
from app.models import Employee, Skill

@bp.route('/dashboard')
def dashboard():
    """Delivery lead dashboard showing managers and their teams."""
    dl_name = request.args.get('dl', 'Robert Zane')

    # Get all managers under this DL
    manager_names = get_managers_by_dl(dl_name)

    # Build hierarchical data
    managers_data = []
    for mgr in manager_names:
        emp_list = get_employees_by_manager(mgr)
        employees_summary = get_employee_summary(emp_list)

        managers_data.append({
            'name': mgr,
            'nbk': emp_list[0].nbk if emp_list else '',
            'role': emp_list[0].role if emp_list else '',
            'employees': employees_summary,
            'total_reports': len(employees_summary),
            'total_gaps': sum(e['current_gaps'] for e in employees_summary)
        })

    # Apply filters
    manager_filter = request.args.get('manager', '')
    employee_filter = request.args.get('employee', '')
    search = request.args.get('search', '').lower()

    if manager_filter:
        managers_data = [m for m in managers_data if m['name'] == manager_filter]

    return render_template('delivery_lead/dashboard.html',
                         dl_name=dl_name,
                         managers=managers_data,
                         all_managers=manager_names)

@bp.route('/employee/<nbk>')
def employee_details(nbk):
    """Employee details view for delivery lead."""
    context = get_employee_details_context(nbk)
    if not context:
        return render_template('errors/404.html'), 404

    return render_template('delivery_lead/employee_details.html',
                         dl_name='Robert Zane',
                         **context)

@bp.route('/reports')
def reports():
    """Delivery lead reports view."""
    dl_name = request.args.get('dl', 'Robert Zane')
    
    employees = Employee.query.filter_by(dl_name=dl_name).all()
    total_employees = len(employees)
    
    total_skills = Skill.query.join(Employee).filter(Employee.dl_name == dl_name).count()
    current_gaps = Skill.query.join(Employee).filter(Employee.dl_name == dl_name, Skill.gap_current == 'Under-Skilled').count()

    return render_template('delivery_lead/reports.html',
                         dl_name=dl_name,
                         total_employees=total_employees,
                         total_skills=total_skills,
                         current_gaps=current_gaps)

@bp.route('/import-data')
def import_data():
    """Delivery lead data import view."""
    return render_template('delivery_lead/import_data.html')

@bp.route('/settings')
def settings():
    """Delivery lead settings view."""
    dl_name = request.args.get('dl', 'Robert Zane')
    return render_template('delivery_lead/settings.html', dl_name=dl_name)
