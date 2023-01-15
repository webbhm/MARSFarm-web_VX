from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime

exp_charts_blueprint = Blueprint('exp_charts_blueprint', __name__, template_folder='templates')

# Page functions
# Charts
#from exp_charts.functions.Ploty_Chart import test_chart_json, env_chart_json


# This is working
@exp_charts_blueprint.route('/exp')
def index():
    try:
        print('exp/index.html')
        return render_template('exp_charts/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@exp_charts_blueprint.route('/exp/', defaults={'page': 'index'})
@exp_charts_blueprint.route('/exp/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('exp_charts/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
        
#--------------- Experiment Charts below here --------------------------
        