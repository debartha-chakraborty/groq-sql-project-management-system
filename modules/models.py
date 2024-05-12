from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Import SQLAlchemy instance from your app


class Employee(db.Model):
    __tablename__ = 'employee'  # Set table name

    emp_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    designation = db.Column(db.String(60), nullable=False)
    skills = db.Column(db.Text)
    active_project_count = db.Column(db.Integer)

    # Relationship with Job table (one-to-many)
    jobs = db.relationship('Job', backref='employee')

    def __repr__(self):
        return f"<Employee {self.emp_id}: {self.name}>"


class Task(db.Model):
    __tablename__ = 'task'  # Set table name

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    request_date = db.Column(db.DateTime)
    tech = db.Column(db.Text, nullable=False)
    ideal_skills = db.Column(db.Text, nullable=False)

    # Relationship with Job table (one-to-many)
    jobs = db.relationship('Job', backref='task')

    def __repr__(self):
        return f"<Task {self.task_id}: {self.title}>"


class Job(db.Model):
    __tablename__ = 'job'  # Set table name

    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), primary_key=True)
    assignment_date = db.Column(db.DateTime)
    estimated_time = db.Column(db.Integer)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(60))

    def __repr__(self):
        return f"<Job: {self.employee.name} - {self.task.title}>"
