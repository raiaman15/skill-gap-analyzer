"""
MyISP Flask Application
Main application file with routes for all user roles.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Load CSV data
def load_data():
    """Load and parse the skill gap CSV data."""
    csv_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    df = pd.read_csv(csv_path)
    return df

# Global data cache (reload on app restart)
df_data = load_data()

def get_employees_by_manager(manager_name):
    """Get all employees reporting to a specific manager."""
    return df_data[df_data['MgrName'] == manager_name]

def get_managers_by_dl(dl_name):
    """Get all managers under a delivery lead."""
    managers = df_data[df_data['DLName'] == dl_name]['MgrName'].unique()
    return [m for m in managers if m != 'N/A']

def get_dls_by_dh(dh_name):
    """Get all delivery leads under a delivery head."""
    dls = df_data[df_data['DHName'] == dh_name]['DLName'].unique()
    return [d for d in dls if d != 'N/A']

def get_dhs_by_gdl(gdl_name):
    """Get all delivery heads under a group delivery lead."""
    dhs = df_data[df_data['GDLName'] == gdl_name]['DHName'].unique()
    return [d for d in dhs if d != 'N/A']

def get_employee_summary(df_subset):
    """Calculate summary stats for a set of employees."""
    if df_subset.empty:
        return []

    employees = []
    for nbk in df_subset['NBK'].unique():
        emp_data = df_subset[df_subset['NBK'] == nbk].iloc[0]
        emp_skills = df_subset[df_subset['NBK'] == nbk]

        current_gaps = (emp_skills['GAP-Current'] == 'Under-Skilled').sum()
        future_gaps = (emp_skills['GAP-Future'] == 'Under-Skilled').sum()
        total_skills = len(emp_skills)

        employees.append({
            'name': emp_data['Name'],
            'nbk': emp_data['NBK'],
            'role': emp_data['Role'],
            'function': emp_data['FunctionName'],
            'manager': emp_data['MgrName'],
            'dl': emp_data['DLName'],
            'dh': emp_data['DHName'],
            'gdl': emp_data['GDLName'],
            'total_skills': total_skills,
            'current_gaps': current_gaps,
            'future_gaps': future_gaps
        })

    return employees

def get_employee_details_context(nbk):
    """Helper to get employee details context."""
    emp_skills = df_data[df_data['NBK'] == nbk]
    if emp_skills.empty:
        return None

    emp_info = emp_skills.iloc[0]
    skills = []
    for _, skill in emp_skills.iterrows():
        skills.append({
            'name': skill['SkillName'],
            'type': skill['SkillType'],
            'category': skill['EmpSkillCategory'],
            'current_prof': skill['User Proficiency'],
            'expected_prof': skill['Expected Current Prof'],
            'gap_current': skill['GAP-Current'],
            'expected_future': skill['Expected Future Prof'],
            'gap_future': skill['GAP-Future']
        })
    
    # Mock feedbacks for now (as per other templates)
    feedbacks = []
    
    return {
        'employee': emp_info.to_dict(),
        'skills': skills,
        'feedbacks': feedbacks
    }

# Index route
@app.route('/')
def index():
    """Landing page with role selection."""
    return render_template('index.html')

# ============================================
# MANAGER ROUTES
# ============================================

@app.route('/manager/dashboard')
def manager_dashboard():
    """Manager dashboard showing direct reports."""
    # For demo, use Harvey Specter as the logged-in manager
    manager_name = request.args.get('manager', 'Harvey Specter')

    # Get employees under this manager
    employees_df = get_employees_by_manager(manager_name)
    employees = get_employee_summary(employees_df)

    # Apply filters if any
    search = request.args.get('search', '').lower()
    employee_filter = request.args.get('employee', '')

    if search:
        employees = [e for e in employees if search in e['name'].lower() or search in e['nbk'].lower()]
    if employee_filter:
        employees = [e for e in employees if e['nbk'] == employee_filter]

    return render_template('manager/dashboard.html',
                         manager_name=manager_name,
                         employees=employees,
                         all_employees=get_employee_summary(employees_df))

@app.route('/manager/employee/<nbk>')
def manager_employee_details(nbk):
    """Employee details view for manager."""
    context = get_employee_details_context(nbk)
    if not context:
        return "Employee not found", 404

    return render_template('manager/employee_details.html',
                         manager_name='Harvey Specter',
                         **context)

@app.route('/manager/reports')
def manager_reports():
    """Manager reports view."""
    manager_name = request.args.get('manager', 'Harvey Specter')
    employees_df = get_employees_by_manager(manager_name)
    employees = get_employee_summary(employees_df)

    # Calculate gap statistics
    total_skills = len(employees_df)
    current_gaps = (employees_df['GAP-Current'] == 'Under-Skilled').sum()

    return render_template('manager/reports.html',
                         manager_name=manager_name,
                         employees=employees,
                         total_skills=total_skills,
                         current_gaps=current_gaps)

@app.route('/manager/import-data')
def manager_import_data():
    """Manager data import view."""
    return render_template('manager/import_data.html')

@app.route('/manager/settings')
def manager_settings():
    """Manager settings view."""
    manager_name = request.args.get('manager', 'Harvey Specter')
    return render_template('manager/settings.html', manager_name=manager_name)

# ============================================
# DELIVERY LEAD ROUTES
# ============================================

@app.route('/delivery-lead/dashboard')
def delivery_lead_dashboard():
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

@app.route('/delivery-lead/employee/<nbk>')
def delivery_lead_employee_details(nbk):
    """Employee details view for delivery lead."""
    context = get_employee_details_context(nbk)
    if not context:
        return "Employee not found", 404

    return render_template('delivery_lead/employee_details.html',
                         dl_name='Robert Zane',
                         **context)

@app.route('/delivery-lead/reports')
def delivery_lead_reports():
    """Delivery lead reports view."""
    dl_name = request.args.get('dl', 'Robert Zane')
    dl_df = df_data[df_data['DLName'] == dl_name]

    total_employees = len(dl_df['NBK'].unique())
    total_skills = len(dl_df)
    current_gaps = (dl_df['GAP-Current'] == 'Under-Skilled').sum()

    return render_template('delivery_lead/reports.html',
                         dl_name=dl_name,
                         total_employees=total_employees,
                         total_skills=total_skills,
                         current_gaps=current_gaps)

@app.route('/delivery-lead/import-data')
def delivery_lead_import_data():
    """Delivery lead data import view."""
    return render_template('delivery_lead/import_data.html')

@app.route('/delivery-lead/settings')
def delivery_lead_settings():
    """Delivery lead settings view."""
    dl_name = request.args.get('dl', 'Robert Zane')
    return render_template('delivery_lead/settings.html', dl_name=dl_name)

# ============================================
# DELIVERY HEAD ROUTES
# ============================================

@app.route('/delivery-head/dashboard')
def delivery_head_dashboard():
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
            emp_df = get_employees_by_manager(mgr)
            employees = get_employee_summary(emp_df)

            managers_data.append({
                'name': mgr,
                'employees': employees,
                'total_reports': len(employees)
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

@app.route('/delivery-head/employee/<nbk>')
def delivery_head_employee_details(nbk):
    """Employee details view for delivery head."""
    context = get_employee_details_context(nbk)
    if not context:
        return "Employee not found", 404

    return render_template('delivery_head/employee_details.html',
                         dh_name='Jessica Pearson',
                         **context)

@app.route('/delivery-head/reports')
def delivery_head_reports():
    """Delivery head reports view."""
    dh_name = request.args.get('dh', 'Jessica Pearson')
    dh_df = df_data[df_data['DHName'] == dh_name]

    return render_template('delivery_head/reports.html',
                         dh_name=dh_name,
                         total_employees=len(dh_df['NBK'].unique()))

@app.route('/delivery-head/import-data')
def delivery_head_import_data():
    """Delivery head data import view."""
    return render_template('delivery_head/import_data.html')

@app.route('/delivery-head/settings')
def delivery_head_settings():
    """Delivery head settings view."""
    dh_name = request.args.get('dh', 'Jessica Pearson')
    return render_template('delivery_head/settings.html', dh_name=dh_name)

# ============================================
# GROUP DELIVERY LEAD ROUTES
# ============================================

@app.route('/group-delivery-lead/dashboard')
def group_delivery_lead_dashboard():
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

@app.route('/group-delivery-lead/employee/<nbk>')
def group_delivery_lead_employee_details(nbk):
    """Employee details view for group delivery lead."""
    context = get_employee_details_context(nbk)
    if not context:
        return "Employee not found", 404

    return render_template('group_delivery_lead/employee_details.html',
                         gdl_name='Daniel Hardman',
                         **context)

@app.route('/group-delivery-lead/reports')
def group_delivery_lead_reports():
    """Group delivery lead reports view."""
    return render_template('group_delivery_lead/reports.html')

@app.route('/group-delivery-lead/import-data')
def group_delivery_lead_import_data():
    """Group delivery lead data import view."""
    return render_template('group_delivery_lead/import_data.html')

@app.route('/group-delivery-lead/settings')
def group_delivery_lead_settings():
    """Group delivery lead settings view."""
    return render_template('group_delivery_lead/settings.html')

# ============================================
# EMPLOYEE ROUTES
# ============================================

@app.route('/employee/dashboard')
def employee_dashboard():
    """Employee dashboard showing personal skills."""
    nbk = request.args.get('nbk', 'mr002')
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return "Employee not found", 404

    emp_info = emp_df.iloc[0]
    skills = []
    current_gaps = 0
    future_gaps = 0

    for _, skill in emp_df.iterrows():
        skills.append({
            'name': skill['SkillName'],
            'current_prof': skill['User Proficiency'],
            'expected_prof': skill['Expected Current Prof'],
            'gap_current': skill['GAP-Current'],
            'gap_future': skill['GAP-Future']
        })
        if skill['GAP-Current'] == 'Under-Skilled':
            current_gaps += 1
        if skill['GAP-Future'] == 'Under-Skilled':
            future_gaps += 1

    return render_template('employee/dashboard.html',
                         employee=emp_info.to_dict(),
                         skills=skills,
                         total_skills=len(skills),
                         current_gaps=current_gaps,
                         future_gaps=future_gaps)

@app.route('/employee/feedback')
def employee_feedback():
    """Employee feedback view."""
    nbk = request.args.get('nbk', 'mr002')
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return "Employee not found", 404

    emp_info = emp_df.iloc[0]
    return render_template('employee/feedback.html', employee=emp_info.to_dict())

@app.route('/employee/upskill-plan')
def employee_upskill_plan():
    """Employee upskill plan view."""
    nbk = request.args.get('nbk', 'mr002')
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return "Employee not found", 404

    emp_info = emp_df.iloc[0]
    # Get skills with current gaps
    skills_with_gaps = emp_df[emp_df['GAP-Current'] == 'Under-Skilled']

    gap_skills = []
    for _, skill in skills_with_gaps.iterrows():
        gap_skills.append({
            'name': skill['SkillName'],
            'current': skill['User Proficiency'],
            'target': skill['Expected Current Prof']
        })

    # Get skills with future gaps (excluding those already in current gaps)
    current_gap_names = set(s['name'] for s in gap_skills)
    future_with_gaps = emp_df[
        (emp_df['GAP-Future'] == 'Under-Skilled') &
        (~emp_df['SkillName'].isin(current_gap_names))
    ]

    future_gap_skills = []
    for _, skill in future_with_gaps.iterrows():
        future_gap_skills.append({
            'name': skill['SkillName'],
            'current': skill['User Proficiency'],
            'target': skill['Expected Future Prof']
        })

    return render_template('employee/upskill_plan.html',
                         employee=emp_info.to_dict(),
                         gap_skills=gap_skills,
                         future_gap_skills=future_gap_skills)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
