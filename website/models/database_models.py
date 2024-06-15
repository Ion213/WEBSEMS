from website import db
from sqlalchemy.sql import func
from pytz import timezone
import datetime

manila_tz = timezone('Asia/Manila')

class Event_name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_N = db.Column(db.String(255),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz).replace(second=0, microsecond=0))
    
#parent of event fees,payments,attendance
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255),nullable=False)
    scheduled_start_date = db.Column(db.DateTime, nullable=False)
    scheduled_end_date = db.Column(db.DateTime, nullable=False)
    event_activities = db.relationship('Event_activity', backref='event', lazy=True)
    event_fees = db.relationship('Event_fees', backref='event', lazy=True)
    payments = db.relationship('Payment', backref='event', lazy=True)
    attendances = db.relationship('Attendance', backref='event', lazy=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz).replace(second=0, microsecond=0))
 
  # child event   
class Event_activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    activity_name = db.Column(db.String(255),nullable=False)
    scheduled_start_time = db.Column(db.Time, nullable=False)
    scheduled_end_time = db.Column(db.Time, nullable=False)
    fines = db.Column(db.Float, nullable=False)

 # child event   
class Event_fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    fee_name = db.Column(db.String(255),nullable=False)
    amount = db.Column(db.Float, nullable=False)

    
#child of event
#child of student
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    date_paid = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz))

#child of event
#child of student
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_marked = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz))
   
#parent of student 
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(100), nullable=True)
    students = db.relationship('Student', backref='department', lazy=True)

#child of department
#parent of attendance      
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz))
    attendances = db.relationship('Attendance', backref='student', lazy=True)

class Ssg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssg_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz))

    