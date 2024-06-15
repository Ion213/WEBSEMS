#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )

from sqlalchemy import func
from datetime import datetime,time
from sqlalchemy import or_,and_,extract
from website import db
from website.models.database_models import Event, Event_activity


admin_manage_activities = Blueprint('admin_manage_activities', __name__)

#add event activity
@admin_manage_activities.route('/add_activity/<int:event_id>', methods=['GET', 'POST'])
@login_required
def add_activity(event_id):
    event = Event.query.get(event_id)
    all_activities = Event_activity.query.filter_by(event_id=event_id).all()

    if request.method == 'POST':
        try:
            activity_name = request.form.get('activity_name')
            activity_start_time_str = request.form.get('activity_start_time')
            activity_end_time_str = request.form.get('activity_end_time')
            fines = float(request.form.get('fines', 0.0))
            
            if not activity_name:
                flash('activity name cannot be empty', category='manage_activity_error')  
            elif not fines:
                flash('fines amount cannot be empty', category='manage_activity_error')
            elif not activity_start_time_str:
                flash('activity start time cannot be empty', category='manage_activity_error')  
            elif not activity_end_time_str:
                flash('activity end time cannot be empty', category='manage_activity_error')
  
            else:                             
                start_time = datetime.strptime(activity_start_time_str, '%H:%M').time()
                end_time = datetime.strptime(activity_end_time_str, '%H:%M').time()

                if start_time >= end_time:
                    flash('Activity start time must be before the end date', category='manage_activity_error')   
                elif end_time <= start_time:
                    flash('Activity end time must be after start date', category='manage_activity_error')  
                else:

                    existing_activity = Event_activity.query.filter_by(event_id=event_id, activity_name=activity_name).first()
                    if existing_activity:
                        flash('An activity with the same name already exists in this event', category='manage_activity_error')
                    else:
                        conflicting_activity = Event_activity.query.filter(
                            Event_activity.event_id == event_id,
                            or_(
                                and_(
                                    Event_activity.scheduled_start_time <= end_time,
                                    Event_activity.scheduled_end_time >= start_time
                                )
                            )
                        ).all()

                        if conflicting_activity:
                            flash('There is a time conflict with existing activity', category='manage_activity_error')
                        else:
                            activity = Event_activity(event_id=event.id,activity_name=activity_name, scheduled_start_time=start_time, scheduled_end_time=end_time, fines=fines)
                            db.session.add(activity)
                            db.session.commit()
                            flash('CREATE SUCCESSFULLY', category='manage_activity_success')
                            return redirect(url_for('admin_manage_activities.add_activity',event_id=event.id))

        except Exception as e:
            flash(str(e), category='manage_activity_error')
            print(e)

    return render_template('admin_event_activities.html',event=event, activities=all_activities)


#delete event activity
# Delete event activity
@admin_manage_activities.route('/delete_event_activity/<int:activity_id>', methods=['POST'])
@login_required
def delete_event_activity(activity_id):
    if request.method == 'POST':
        try:
            activity = Event_activity.query.get(activity_id)
            if activity:
                db.session.delete(activity)
                db.session.commit()
                flash('Event activity deleted successfully', category='manage_activity_success')
                return redirect(url_for('admin_manage_activities.add_activity', event_id=activity.event_id if activity else None))
            else:
                flash('Event activity not found', category='manage_activity_error')
            
        
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash(str(e), category='manage_activity_error')
            
    return redirect(url_for('admin_manage_activities.add_activity'))