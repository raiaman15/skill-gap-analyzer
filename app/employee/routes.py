from flask import Blueprint, render_template, request
from app.utils import get_data, get_employee_details_context

bp = Blueprint('employee', __name__, url_prefix='/employee')

@bp.route('/dashboard')
def dashboard():
    """Employee dashboard showing personal skills."""
    nbk = request.args.get('nbk', 'mr002')
    df_data = get_data()
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return render_template('errors/404.html'), 404

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

@bp.route('/feedback')
def feedback():
    """Employee feedback view."""
    nbk = request.args.get('nbk', 'mr002')
    df_data = get_data()
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return render_template('errors/404.html'), 404

    emp_info = emp_df.iloc[0]
    return render_template('employee/feedback.html', employee=emp_info.to_dict())

@bp.route('/upskill-plan')
def upskill_plan():
    """Employee upskill plan view."""
    nbk = request.args.get('nbk', 'mr002')
    df_data = get_data()
    emp_df = df_data[df_data['NBK'] == nbk]

    if emp_df.empty:
        return render_template('errors/404.html'), 404

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
