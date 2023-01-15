from flask import Blueprint, render_template, abort
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
        

