from flask import Blueprint, render_template, abort, request, session, redirect, url_for
from jinja2 import TemplateNotFound

admin_blueprint = Blueprint('admin_blueprint', __name__, template_folder='templates')

# This is working
@admin_blueprint.route('/admin')
def index():
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for index.html')
        return render_template('admin/index.html', data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

# Now working
@admin_blueprint.route('/admin/', defaults={'page': 'index'})
@admin_blueprint.route('/admin/url', defaults={'page': 'url'})
@admin_blueprint.route('/admin/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('admin/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
# ----------------- MARSFarm specific stuff -----------------        
@admin_blueprint.route('/admin/set_login', methods=['GET', 'POST'])
def set_login():
    # save the email to the session
    print("Set Login")
    print("Method", request.method)
    if request.method == 'POST':
        print("POST: Set session")
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        print("Return redirect")
        return redirect(url_for('admin_blueprint.get_login'))

    return render_template('/admin/login.html')

@admin_blueprint.route('/admin/get_login', methods=['GET', 'POST'])
def get_login():
    # get login information
    print("Get Login")
    return render_template('/admin/set_login.html')

@admin_blueprint.route('/admin/logout')
def logout():
    # Clear the email stored in the session object
    print("Logout")
    session.pop('email', default=None)
    return render_template('/admin/logout.html')