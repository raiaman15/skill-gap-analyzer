from app import db
from app.models import Employee, Skill, Feedback

def get_employees_by_manager(manager_name):
    """Get all employees reporting to a specific manager."""
    return Employee.query.filter_by(manager_name=manager_name).all()

def get_managers_by_dl(dl_name):
    """Get all managers under a delivery lead."""
    # Query distinct manager names where dl_name matches
    result = db.session.query(Employee.manager_name).filter_by(dl_name=dl_name).distinct().all()
    # result is a list of tuples like [('Harvey Specter',), ...]
    return [r[0] for r in result if r[0] and r[0] != 'N/A']

def get_dls_by_dh(dh_name):
    """Get all delivery leads under a delivery head."""
    result = db.session.query(Employee.dl_name).filter_by(dh_name=dh_name).distinct().all()
    return [r[0] for r in result if r[0] and r[0] != 'N/A']

def get_dhs_by_gdl(gdl_name):
    """Get all delivery heads under a group delivery lead."""
    result = db.session.query(Employee.dh_name).filter_by(gdl_name=gdl_name).distinct().all()
    return [r[0] for r in result if r[0] and r[0] != 'N/A']

def get_employee_summary(employees):
    """
    Calculate summary stats for a list of Employee objects.
    Returns a list of dictionaries with summary data.
    """
    if not employees:
        return []

    summary_list = []
    for emp in employees:
        # Count skills and gaps
        # We could optimize this with a join or aggregation query, but loop is fine for now
        skills = Skill.query.filter_by(employee_nbk=emp.nbk).all()
        
        total_skills = len(skills)
        current_gaps = sum(1 for s in skills if s.gap_current == 'Under-Skilled')
        future_gaps = sum(1 for s in skills if s.gap_future == 'Under-Skilled')

        summary_list.append({
            'name': emp.name,
            'nbk': emp.nbk,
            'role': emp.role,
            'function': emp.function_name,
            'manager': emp.manager_name,
            'dl': emp.dl_name,
            'dh': emp.dh_name,
            'gdl': emp.gdl_name,
            'total_skills': total_skills,
            'current_gaps': current_gaps,
            'future_gaps': future_gaps
        })

    return summary_list

def get_employee_details_context(nbk):
    """Helper to get employee details context."""
    emp = Employee.query.get(nbk)
    if not emp:
        return None

    skills_query = Skill.query.filter_by(employee_nbk=nbk).all()
    
    skills = []
    for skill in skills_query:
        skills.append({
            'name': skill.skill_name,
            'type': skill.skill_type,
            'category': skill.emp_skill_category,
            'current_prof': skill.user_proficiency,
            'expected_prof': skill.expected_current_prof,
            'gap_current': skill.gap_current,
            'expected_future': skill.expected_future_prof,
            'gap_future': skill.gap_future
        })
    
    # Fetch feedbacks
    feedbacks_query = Feedback.query.filter_by(employee_nbk=nbk).order_by(Feedback.created_at.desc()).all()
    feedbacks = [{
        'given_by': f.given_by,
        'feedback_type': f.feedback_type,
        'content': f.content,
        'date': f.created_at
    } for f in feedbacks_query]
    
    # Map Employee object to dict with Capitalized keys to match legacy template expectations
    # This avoids breaking all templates that use {{ employee.Name }} etc.
    employee_dict = {
        'Name': emp.name,
        'NBK': emp.nbk,
        'Email': emp.email,
        'Role': emp.role,
        'FunctionName': emp.function_name,
        'PM/IC': emp.pm_ic,
        'MgrName': emp.manager_name,
        'DLName': emp.dl_name,
        'DHName': emp.dh_name,
        'GDLName': emp.gdl_name
    }
    
    return {
        'employee': employee_dict,
        'skills': skills,
        'feedbacks': feedbacks
    }
