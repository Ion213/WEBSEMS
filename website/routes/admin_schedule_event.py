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
from datetime import datetime
from sqlalchemy import or_,and_,extract
from website import db
from website.models.database_models import Event_name,Event, Event_fees,Event_activity


admin_schedule_event = Blueprint('admin_schedule_event', __name__)

#add sched event
@admin_schedule_event.route('/schedule_event', methods=['GET', 'POST'])
@login_required
def schedule_event():
    if request.method == 'POST':
        try:
            eventname = request.form.get('Eventname')
            scheduled_start_date_str = request.form.get('scheduled_start_date')
            scheduled_end_date_str = request.form.get('scheduled_end_date')
            
            if not eventname:
                flash('event name cannot be empty', category='schedule_event_error')  
            elif not scheduled_start_date_str:
                flash('event start date cannot be empty', category='schedule_event_error')  
            elif not scheduled_end_date_str:
                flash('event end adte cannot be empty', category='schedule_event_error') 
            else:                             
                scheduled_start_date = datetime.strptime(scheduled_start_date_str, '%Y-%m-%d')
                scheduled_end_date = datetime.strptime(scheduled_end_date_str, '%Y-%m-%d')
                
                start=scheduled_start_date.date()

                if start < datetime.now().date():
                    flash('Scheduled start time must be in the future', category='schedule_event_error')  
                elif scheduled_start_date > scheduled_end_date:
                    flash('Scheduled start date must be before the end date', category='schedule_event_error')   
                elif scheduled_end_date < scheduled_start_date:
                    flash('Scheduled end date must be after start date', category='schedule_event_error')  
                else:
                    # Check for conflicting events

                    conflicting_events = Event.query.filter(
                        or_(
                            and_(

                                Event.scheduled_start_date <= scheduled_end_date,
                                Event.scheduled_end_date >= scheduled_start_date
                            )
                        )
                    ).all()

                    if conflicting_events:
                        flash('There is a time conflict with existing events', category='schedule_event_error')
                    else:
                        
                        existing_event = Event.query.filter(
                            Event.event_name == eventname,
                            extract('year', Event.scheduled_start_date) == scheduled_start_date.year
                        ).first()
                        
                        if existing_event:
                            flash('Event name already in the current year', category='schedule_event_error')
                        else:
                            event = Event(event_name=eventname, scheduled_start_date=scheduled_start_date, scheduled_end_date=scheduled_end_date)
                            db.session.add(event)
                            db.session.commit()
                            flash('CREATE SUCCESSFULLY', category='schedule_event_success')

        except Exception as e:
            flash(str(e), category='schedule_event_error')
    
    event_names= Event_name.query.order_by(Event_name.event_N.asc()).all()       
    events = Event.query.order_by(Event.event_name.asc()).all()
    
    total_amounts = {}
    for event in events:
        total_amounts[event.id] = db.session.query(func.sum(Event_fees.amount)).filter_by(event_id=event.id).scalar() or 0
    
    return render_template('admin_schedule_event.html',events=events,total_amounts=total_amounts,event_names=event_names)

#delete sched event
@admin_schedule_event.route('/delete_scheduled_event/<int:event_id>', methods=['POST'])
@login_required
def delete_scheduled_event(event_id):
    if request.method == 'POST':
        try:
            event = Event.query.get(event_id)
            Event_fees.query.filter_by(event_id=event.id).delete()
            Event_activity.query.filter_by(event_id=event.id).delete()
            db.session.delete(event)
            db.session.commit()
            flash('Event deleted successfully',category='schedule_event_success')
            return redirect(url_for('admin_schedule_event.schedule_event'))
        
        except Exception as e:
            flash(str(e), category='schedule_event_error')
            
    events = Event.query.all()
    return redirect(url_for('admin_schedule_event.schedule_event',events=events))

# Update scheduled event
@admin_schedule_event.route('/update_schedule_event/', methods=['POST'])
@login_required
def update_schedule_event():
    if request.method == 'POST':
        try:
            
            event_schedule_id=request.form.get('update_event_schedule_id')
            new_event_name= request.form.get('update_event_schedule_name')
            new_event_start_str= request.form.get('update_event_schedule_start')
            new_event_end_str= request.form.get('update_event_schedule_end')

            if not new_event_name:
                flash('Event name cannot be empty', category='schedule_event_error')
                return redirect(url_for('admin_schedule_event.schedule_event'))
            elif not new_event_start_str:
                flash('Event start date cannot be empty', category='schedule_event_error')
                return redirect(url_for('admin_schedule_event.schedule_event'))
            elif not new_event_end_str:
                flash('Event end date cannot be empty', category='schedule_event_error')
                return redirect(url_for('admin_schedule_event.schedule_event'))
            else:
                new_event_start = datetime.strptime(new_event_start_str, '%Y-%m-%d')
                new_event_end = datetime.strptime(new_event_end_str, '%Y-%m-%d')
                
                existing_event = Event.query.filter(Event.id != event_schedule_id, Event.event_name == new_event_name).first()
                if existing_event:
                    flash('Event name already exists', category='schedule_event_error')
                    return redirect(url_for('admin_schedule_event.schedule_event'))
                    
                conflicting_events = Event.query.filter(
                    and_(
                        Event.id != event_schedule_id,
                        or_(
                            and_(
                                Event.scheduled_start_date <= new_event_end,
                                Event.scheduled_end_date >= new_event_start
                            )
                        )
                    )
                ).all()

                if conflicting_events:
                        flash('There is a time conflict with existing events', category='schedule_event_error')
                        return redirect(url_for('admin_schedule_event.schedule_event'))
                else:
                    event = Event.query.get(event_schedule_id)
                    event.event_name = new_event_name
                    event.schedule_start_date = new_event_start
                    event.scheduled_end_date = new_event_end
                    db.session.commit()
                    flash('Event updated successfully', category='schedule_event_success')
                    return redirect(url_for('admin_schedule_event.schedule_event'))

        except Exception as e:
            flash(str(e), category='schedule_event_error')

    return redirect(url_for('admin_schedule_event.schedule_event'))

