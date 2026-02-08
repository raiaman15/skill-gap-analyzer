from flask import Blueprint, render_template, request
from app.utils import get_dhs_by_gdl, get_dls_by_dh, get_managers_by_dl, get_employees_by_manager, get_employee_summary, get_employee_details_context

bp = Blueprint('group_delivery_lead', __name__, url_prefix='/group-delivery-lead')

@bp.route('/dashboard')
def dashboard():
    """Group delivery lead dashboard showing complete enterprise hierarchy."""
    gdl_name = request.args.get('gdl', 'Daniel Hardman')

    # Get DHs under this GDL
    dh_names = get_dhs_by_gdl(gdl_name)

    dhs_data = []
    for dh in dh_names:
        dl_names = get_dls_by_dh(dh)
        dls_data = []

        for dl in dl_names:
            manager_names = get_managers_by_dl(dl)
            managers_data = []

            for mgr in manager_names:
                emp_df = get_employees_by_manager(mgr)
                employees = get_employee_summary(emp_df)
                managers_data.append({
                    'name': mgr,
                    'employees': employees
                })

            dls_data.append({
                'name': dl,
                'managers': managers_data
            })

        dhs_data.append({
            'name': dh,
            'dls': dls_data
        })

    return render_template('group_delivery_lead/dashboard.html',
                         gdl_name=gdl_name,
                         dhs=dhs_data)

@bp.route('/employee/<nbk>')
def employee_details(nbk):
    """Employee details view for group delivery lead."""
    context = get_employee_details_context(nbk)
    if not context:
        return render_template('errors/404.html'), 404

    return render_template('group_delivery_lead/employee_details.html',
                         gdl_name='Daniel Hardman',
                         **context)

@bp.route('/reports')
def reports():
    """Group delivery lead reports view."""
    return render_template('group_delivery_lead/reports.html')

@bp.route('/import-data')
def import_data():
    """Group delivery lead data import view."""
    return render_template('group_delivery_lead/import_data.html')

@bp.route('/settings')
def settings():
    """Group delivery lead settings view."""
    return render_template('group_delivery_lead/settings.html')
