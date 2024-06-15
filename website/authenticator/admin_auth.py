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
import pyrebase

#your firebase config
config = {
    "apiKey": "AIzaSyDIsfXBQDrQkbFumh8FvWMtWKOT-k4Oo5E",
    "authDomain": "dtcweb-f3c53.firebaseapp.com",
    "databaseURL": "",  # Not needed for Pyrebase
    "projectId": "dtcweb-f3c53",
    "storageBucket": "dtcweb-f3c53.appspot.com",
    "messagingSenderId": "322330767293",
    "appId": "1:322330767293:web:56ead0c7729f473dcbacd4",
    "measurementId": "G-X9T862VDS0"
}
#initialize the config
firebase = pyrebase.initialize_app(config)
#create a variable to the initialized config
auth = firebase.auth()

#create blueprint/routes
admin_auth = Blueprint('admin_auth', __name__)

@admin_auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user= auth.sign_in_with_email_and_password(email, password)
            session_id = user['localId']
            from website.security.session_storage import User
            login_user(User(session_id))
            flash('Log in successfully!', category='login_success')
            return redirect(url_for('admin_schedule_event.schedule_event'))
        except Exception as e:
            flash(f'{e}', category='login_error')
            
    return render_template('admin_login.html')

#admin logout route
@admin_auth.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_auth.admin_login'))