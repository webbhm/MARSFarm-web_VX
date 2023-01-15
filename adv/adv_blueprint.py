from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

adv_blueprint = Blueprint('adv_blueprint', __name__, template_folder='templates')

# This is working
@adv_blueprint.route('/adv')
def index():
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for index.html')
        return render_template('adv/index.html', data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

# Now working
@adv_blueprint.route('/adv/', defaults={'page': 'index'})
@adv_blueprint.route('/adv/url', defaults={'page': 'url'})
@adv_blueprint.route('/adv/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('adv/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        

