from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    nbk = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(100))
    function_name = db.Column(db.String(100))
    pm_ic = db.Column(db.String(10)) # PM or IC
    manager_name = db.Column(db.String(100)) # Storing name for now as per CSV
    dl_name = db.Column(db.String(100))
    dh_name = db.Column(db.String(100))
    gdl_name = db.Column(db.String(100))

    # Relationships can be added later if we normalize manager/DL/DH/GDL into separate tables
    # or self-referential relationships if everyone is an employee.
    # For now, following the flat structure implied by CSV import ease.

    skills = db.relationship('Skill', backref='employee', lazy=True)
    training_plans = db.relationship('TrainingPlan', backref='employee', lazy=True)
    feedbacks = db.relationship('Feedback', backref='employee', lazy=True)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    employee_nbk = db.Column(db.String(20), db.ForeignKey('employees.nbk'), nullable=False)
    skill_name = db.Column(db.String(100))
    skill_type = db.Column(db.String(50))
    emp_skill_category = db.Column(db.String(50))
    user_proficiency = db.Column(db.String(50))
    expected_current_prof = db.Column(db.String(50))
    gap_current = db.Column(db.String(20))
    expected_future_prof = db.Column(db.String(50))
    gap_future = db.Column(db.String(20))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'
    id = db.Column(db.Integer, primary_key=True)
    employee_nbk = db.Column(db.String(20), db.ForeignKey('employees.nbk'), nullable=False)
    skill_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Not Started')
    assigned_by = db.Column(db.String(100))
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_proficiency = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    completion_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    milestones = db.relationship('Milestone', backref='training_plan', lazy=True)

class Milestone(db.Model):
    __tablename__ = 'milestones'
    id = db.Column(db.Integer, primary_key=True)
    training_plan_id = db.Column(db.Integer, db.ForeignKey('training_plans.id'), nullable=False)
    title = db.Column(db.String(100))
    target_level = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    employee_nbk = db.Column(db.String(20), db.ForeignKey('employees.nbk'), nullable=False)
    given_by = db.Column(db.String(100))
    feedback_type = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DataImportLog(db.Model):
    __tablename__ = 'data_import_logs'
    id = db.Column(db.Integer, primary_key=True)
    imported_by = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    row_count = db.Column(db.Integer)
    status = db.Column(db.String(20))
    imported_at = db.Column(db.DateTime, default=datetime.utcnow)
    error_message = db.Column(db.Text)

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    email_notifications = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrainingResource(db.Model):
    __tablename__ = 'training_resources'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100))
    tier = db.Column(db.String(50))
    resource_url_1 = db.Column(db.String(255))
    resource_url_2 = db.Column(db.String(255))
