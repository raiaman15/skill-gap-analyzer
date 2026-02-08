from flask import Blueprint, render_template, request
from app.utils import get_dls_by_dh, get_managers_by_dl, get_employees_by_manager, get_employee_summary, get_employee_details_context
from app.models import Employee

bp = Blueprint('delivery_head', __name__, url_prefix='/delivery-head')

@bp.route('/dashboard')
def dashboard():
    """Delivery head dashboard showing full hierarchy."""
    dh_name = request.args.get('dh', 'Jessica Pearson')

    # Get DLs under this DH
    dl_names = get_dls_by_dh(dh_name)

    dls_data = []
    for dl in dl_names:
        # Get managers under this DL
        manager_names = get_managers_by_dl(dl)
        managers_data = []

        for mgr in manager_names:
            emp_list = get_employees_by_manager(mgr)
            employees_summary = get_employee_summary(emp_list)

            managers_data.append({
                'name': mgr,
                'employees': employees_summary,
                'total_reports': len(employees_summary)
            })

        dls_data.append({
            'name': dl,
            'managers': managers_data,
            'total_managers': len(managers_data),
            'total_employees': sum(m['total_reports'] for m in managers_data)
        })

    return render_template('delivery_head/dashboard.html',
                         dh_name=dh_name,
                         dls=dls_data)

@bp.route('/employee/<nbk>')
def employee_details(nbk):
    """Employee details view for delivery head."""
    context = get_employee_details_context(nbk)
    if not context:
        return render_template('errors/404.html'), 404

    return render_template('delivery_head/employee_details.html',
                         dh_name='Jessica Pearson',
                         **context)

@bp.route('/reports')
def reports():
    """Delivery head reports view."""
    dh_name = request.args.get('dh', 'Jessica Pearson')
    
    total_employees = Employee.query.filter_by(dh_name=dh_name).count()

    return render_template('delivery_head/reports.html',
                         dh_name=dh_name,
                         total_employees=total_employees)

@bp.route('/import-data')
def import_data():
    """Delivery head data import view."""
    return render_template('delivery_head/import_data.html')

@bp.route('/settings')
def settings():
    """Delivery head settings view."""
    dh_name = request.args.get('dh', 'Jessica Pearson')
    return render_template('delivery_head/settings.html', dh_name=dh_name)
