from flask import render_template, request
from app.employee import bp
from app.models import Employee, Skill

def get_employee_dict(emp):
    """Helper to map Employee object to dict with capitalized keys for templates."""
    return {
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

@bp.route('/dashboard')
def dashboard():
    """Employee dashboard showing personal skills."""
    nbk = request.args.get('nbk', 'mr002')
    emp = Employee.query.get(nbk)

    if not emp:
        return render_template('errors/404.html'), 404

    emp_dict = get_employee_dict(emp)
    skills_query = Skill.query.filter_by(employee_nbk=nbk).all()
    
    skills = []
    current_gaps = 0
    future_gaps = 0

    for skill in skills_query:
        skills.append({
            'name': skill.skill_name,
            'current_prof': skill.user_proficiency,
            'expected_prof': skill.expected_current_prof,
            'gap_current': skill.gap_current,
            'gap_future': skill.gap_future
        })
        if skill.gap_current == 'Under-Skilled':
            current_gaps += 1
        if skill.gap_future == 'Under-Skilled':
            future_gaps += 1

    return render_template('employee/dashboard.html',
                         employee=emp_dict,
                         skills=skills,
                         total_skills=len(skills),
                         current_gaps=current_gaps,
                         future_gaps=future_gaps)

@bp.route('/feedback')
def feedback():
    """Employee feedback view."""
    nbk = request.args.get('nbk', 'mr002')
    emp = Employee.query.get(nbk)

    if not emp:
        return render_template('errors/404.html'), 404

    return render_template('employee/feedback.html', employee=get_employee_dict(emp))

@bp.route('/upskill-plan')
def upskill_plan():
    """Employee upskill plan view."""
    nbk = request.args.get('nbk', 'mr002')
    emp = Employee.query.get(nbk)

    if not emp:
        return render_template('errors/404.html'), 404

    skills_query = Skill.query.filter_by(employee_nbk=nbk).all()

    gap_skills = []
    future_gap_skills = []
    
    # Track names to avoid duplicates if logic requires, though usually gap_future check excludes current gaps
    # The original logic was:
    # future_with_gaps = emp_df[
    #    (emp_df['GAP-Future'] == 'Under-Skilled') &
    #    (~emp_df['SkillName'].isin(current_gap_names))
    # ]
    
    current_gap_names = set()

    # First pass for current gaps
    for skill in skills_query:
        if skill.gap_current == 'Under-Skilled':
            gap_skills.append({
                'name': skill.skill_name,
                'current': skill.user_proficiency,
                'target': skill.expected_current_prof
            })
            current_gap_names.add(skill.skill_name)

    # Second pass for future gaps
    for skill in skills_query:
        if skill.gap_future == 'Under-Skilled' and skill.skill_name not in current_gap_names:
            future_gap_skills.append({
                'name': skill.skill_name,
                'current': skill.user_proficiency,
                'target': skill.expected_future_prof
            })

    return render_template('employee/upskill_plan.html',
                         employee=get_employee_dict(emp),
                         gap_skills=gap_skills,
                         future_gap_skills=future_gap_skills)
