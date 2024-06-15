#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash,
    jsonify
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )

from datetime import datetime
from website import db
from website.models.database_models import Event_name

admin_manage_event = Blueprint('admin_manage_event', __name__)


#add event
@admin_manage_event.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        try:
            event_N = request.form.get('eventN')
            existing_event = Event_name.query.filter_by(event_N=event_N).first()
            if existing_event:
                flash('Event name already exists', category='manage_event_error')
            else:
                eventName = Event_name(event_N=event_N)
                db.session.add(eventName)
                db.session.commit()
                flash('CREATE SUCCESSFULLY', category='manage_event_success')

        except Exception as e:
            flash(str(e), category='manage_event_error')
            
    all_event_names = Event_name.query.order_by(Event_name.event_N.asc()).all()
    
    return render_template('admin_manage_event.html',all_event_names=all_event_names)


#delete event
@admin_manage_event.route('/delete_event/<int:event_name_id>', methods=['POST'])
@login_required
def delete_event(event_name_id):
    if request.method == 'POST':
        try:
            event_N = Event_name.query.get(event_name_id)
            db.session.delete(event_N)
            db.session.commit()
            flash('Event deleted successfully',category='schedule_event_success')
            return redirect(url_for('admin_manage_event.add_event'))
        
        except Exception as e:
            flash(str(e), category='schedule_event_error')
            
    all_event_names = Event_name.query.all()
    return redirect(url_for('admin_manage_event.add_event',all_event_names=all_event_names))


# Update event
@admin_manage_event.route('/update_event', methods=['POST'])
@login_required
def update_event():
    if request.method == 'POST':
        try:
            event_id = request.form.get('update_event_id')
            event_N = request.form.get('update_event_name')

            # Check if the event name is empty
            if not event_N:
                flash('Event name cannot be empty', category='manage_event_error')
                return redirect(url_for('admin_manage_event.add_event'))

            # Check if the event name already exists
            existing_event = Event_name.query.filter(Event_name.id != event_id, Event_name.event_N == event_N).first()
            if existing_event:
                flash('Event name already exists', category='manage_event_error')
                return redirect(url_for('admin_manage_event.add_event'))

            event = Event_name.query.get(event_id)
            event.event_N = event_N
            db.session.commit()
            flash('Event updated successfully', category='manage_event_success')
        except Exception as e:
            flash(str(e), category='manage_event_error')
    
    return redirect(url_for('admin_manage_event.add_event'))



