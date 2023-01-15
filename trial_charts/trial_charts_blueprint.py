from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime

trial_charts_blueprint = Blueprint('trial_charts_blueprint', __name__, template_folder='templates')

# Page functions
# Charts
#from trial_charts.functions.Ploty_Chart import test_chart_json, env_chart_json
#from trial_charts.functions.GBE_Data import get_trial
from functions.GBE_Util import *

# This is working
@trial_charts_blueprint.route('/trial')
def index():
    try:
        print('trial_charts/index.html')
        return render_template('trial_charts/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@trial_charts_blueprint.route('/trail/', defaults={'page': 'index'})
@trial_charts_blueprint.route('/trial/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template: %s.html' % page)
        return render_template('trial_charts/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
