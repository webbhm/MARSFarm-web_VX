from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime

chart_blueprint = Blueprint('chart_blueprint', __name__, template_folder='templates')

# Page functions
# Charts
from charts.functions.Ploty_Chart import test_chart_json, env_chart_json
from charts.functions.GBE_Data import get_trial
from functions.GBE_Util import *

# This is working
@chart_blueprint.route('/charts')
def index():
    try:
        print('charts/index.html')
        return render_template('charts/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@chart_blueprint.route('/charts/', defaults={'page': 'index'})
@chart_blueprint.route('/charts/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('charts/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
@chart_blueprint.route('/charts/test_chart', methods=['GET', 'POST'])
def test_chart():
    try:
        graphJSON = test_chart_json()
        print(graphJSON)
        page_data = {}
        print("Render_Template")
        return render_template('charts/test_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        print("Except test_chart", e)
        abort(404)
 
@chart_blueprint.route('/charts/dashboard', methods=['GET', 'POST'])
def dashboard():
    try:
#         data = get_test_data('temperature')
#         page_data = get_page_data()
#         print(page_data)
#         #fig = env_chart(attribute, school, start_date, end_date)
#         graphJSON = get_JSONChart(data, fmt)
#         print("Render_Template")
        return render_template('charts/dashboard.html')
    except Exception as e:
        print("Except dashboard", e)
        abort(404)
        
#--------------- GBE Charts below here --------------------------
        
@chart_blueprint.route('/charts/env', methods=['GET', 'POST'])
def env():
    try:
        # FIX: need to get dates from trial, and attribute from input
        attribute = 'Temperature'
        start_date = (datetime.now().timestamp()-(30*24*60*60))*1000
        end_date = datetime.now().timestamp()*1000
        start_date_str = '12/11/2022'
        end_date_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        graphJSON = env_chart_json(attribute, start_date, end_date)
        print(graphJSON)
        page_data = {'farm':'OpenAgBloom', 'trial':123, 'start_date':start_date_str, 'end_date':end_date_str}
        print("Render_Template")
        return render_template('charts/env_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        print("Except test_chart", e)
        abort(404)    


