import pandas as pd
from app import create_app, db
from app.models import Employee, Skill, TrainingResource
import os

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data? (Optional, be careful in prod)
        # db.drop_all()
        # db.create_all()
        
        # Load sample_data.csv
        base_dir = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.join(base_dir, 'sample_data.csv')
        
        if not os.path.exists(csv_path):
            print(f"Error: {csv_path} not found.")
            return

        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from sample_data.csv")

        # Create Employees (Unique)
        # Assuming one row per employee-skill combo, so we need to deduplicate employees
        employees_df = df.drop_duplicates(subset=['NBK'])
        
        for _, row in employees_df.iterrows():
            employee = Employee(
                nbk=row['NBK'],
                name=row['Name'],
                email=row['Email'],
                role=row['Role'],
                function_name=row['FunctionName'],
                pm_ic=row['PM/IC'],
                manager_name=row['MgrName'],
                dl_name=row['DLName'],
                dh_name=row['DHName'],
                gdl_name=row['GDLName']
            )
            # Check if exists
            existing = Employee.query.get(row['NBK'])
            if not existing:
                db.session.add(employee)
            else:
                # Update?
                pass
        
        db.session.commit()
        print("Employees seeded.")

        # Create Skills
        for _, row in df.iterrows():
            skill = Skill(
                employee_nbk=row['NBK'],
                skill_name=row['SkillName'],
                skill_type=row['SkillType'],
                emp_skill_category=row['EmpSkillCategory'],
                user_proficiency=row['User Proficiency'],
                expected_current_prof=row['Expected Current Prof'],
                gap_current=row['GAP-Current'],
                expected_future_prof=row['Expected Future Prof'],
                gap_future=row['GAP-Future']
            )
            db.session.add(skill)
        
        db.session.commit()
        print("Skills seeded.")

        # Load sample_trainings.csv
        trainings_csv_path = os.path.join(base_dir, 'sample_trainings.csv')
        if os.path.exists(trainings_csv_path):
            df_trainings = pd.read_csv(trainings_csv_path)
            print(f"Loaded {len(df_trainings)} rows from sample_trainings.csv")

            for _, row in df_trainings.iterrows():
                # One row has links for multiple tiers. 
                # I should probably create multiple TrainingResource entries or update the model to support this structure.
                # The model has 'tier', 'resource_url_1', 'resource_url_2'.
                # Maybe I should create 3 resources per row, one for each tier?
                
                tiers = [
                    ('New to Role', row.get('New to Role')),
                    ('In Role Development', row.get('In role Development')),
                    ('Mastery', row.get('Mastery'))
                ]
                
                for tier_name, url in tiers:
                    if pd.notna(url):
                        resource = TrainingResource(
                            skill_name=row['Learning Need'],
                            tier=tier_name,
                            resource_url_1=url,
                            resource_url_2=None # CSV doesn't seem to have a second URL column per tier
                        )
                        db.session.add(resource)
            
            db.session.commit()
            print("Training resources seeded.")
        else:
            print("sample_trainings.csv not found, skipping training resources.")

if __name__ == '__main__':
    seed_data()
