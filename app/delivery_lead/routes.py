from flask import Blueprint, render_template, request
from app.utils import get_data, get_managers_by_dl, get_employees_by_manager, get_employee_summary, get_employee_details_context

bp = Blueprint('delivery_lead', __name__, url_prefix='/delivery-lead')

@bp.route('/dashboard')
def dashboard():
    """Delivery lead dashboard showing managers and their teams."""
    dl_name = request.args.get('dl', 'Robert Zane')

    # Get all managers under this DL
    manager_names = get_managers_by_dl(dl_name)

    # Build hierarchical data
    managers_data = []
    for mgr in manager_names:
        emp_df = get_employees_by_manager(mgr)
        employees = get_employee_summary(emp_df)

        managers_data.append({
            'name': mgr,
            'nbk': emp_df.iloc[0]['NBK'] if not emp_df.empty else '',
            'role': emp_df.iloc[0]['Role'] if not emp_df.empty else '',
            'employees': employees,
            'total_reports': len(employees),
            'total_gaps': sum(e['current_gaps'] for e in employees)
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
    df_data = get_data()
    dl_df = df_data[df_data['DLName'] == dl_name]

    total_employees = len(dl_df['NBK'].unique())
    total_skills = len(dl_df)
    current_gaps = (dl_df['GAP-Current'] == 'Under-Skilled').sum()

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
