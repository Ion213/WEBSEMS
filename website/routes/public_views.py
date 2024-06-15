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


from website.security.limiter import limiter 

public_views = Blueprint('public_views', __name__)

@public_views.route('/', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def home():
    return render_template('home.html', )
