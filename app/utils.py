import pandas as pd
import os

# Global cache
_df_data = None

def load_data():
    """Load and parse the skill gap CSV data."""
    global _df_data
    if _df_data is None:
        # Assuming sample_data.csv is in the root directory relative to this file
        # This file is in app/utils.py, so root is ../
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'sample_data.csv')
        _df_data = pd.read_csv(csv_path)
    return _df_data

def get_data():
    """Get the loaded dataframe."""
    return load_data()

def get_employees_by_manager(manager_name):
    """Get all employees reporting to a specific manager."""
    df = get_data()
    return df[df['MgrName'] == manager_name]

def get_managers_by_dl(dl_name):
    """Get all managers under a delivery lead."""
    df = get_data()
    managers = df[df['DLName'] == dl_name]['MgrName'].unique()
    return [m for m in managers if m != 'N/A']

def get_dls_by_dh(dh_name):
    """Get all delivery leads under a delivery head."""
    df = get_data()
    dls = df[df['DHName'] == dh_name]['DLName'].unique()
    return [d for d in dls if d != 'N/A']

def get_dhs_by_gdl(gdl_name):
    """Get all delivery heads under a group delivery lead."""
    df = get_data()
    dhs = df[df['GDLName'] == gdl_name]['DHName'].unique()
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
    df = get_data()
    emp_skills = df[df['NBK'] == nbk]
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
    
    # Mock feedbacks for now
    feedbacks = []
    
    return {
        'employee': emp_info.to_dict(),
        'skills': skills,
        'feedbacks': feedbacks
    }
