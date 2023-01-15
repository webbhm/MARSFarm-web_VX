from flask import Blueprint, render_template, request, abort
from jinja2 import TemplateNotFound
from datetime import datetime
from gbe_charts.functions.Group_Chart import *
import plotly

gbe_charts_blueprint = Blueprint('gbe_charts_blueprint', __name__, template_folder='templates')

# Page functions
# Charts
#from gbe_charts.functions.Ploty_Chart import test_chart_json, env_chart_json
#from gbe_charts.functions.GBE_Data import get_trial
#from functions.GBE_Util import *

# This is working
@gbe_charts_blueprint.route('/gbe')
def index():
    try:
        print('gbe_charts/index.html')
        return render_template('gbe_charts/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@gbe_charts_blueprint.route('/gbe/', defaults={'page': 'index'})
@gbe_charts_blueprint.route('/gbe/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('gbe_charts/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
#--------------- GBE Charts below here --------------------------
        
@gbe_charts_blueprint.route('/gbe/plant_attr', methods=['GET', 'POST'])
def school_attribute():
    # plant attributes by week (height, width, mass)
    # Move to trial_charts
    school = request.args.get('school')
    attribute = request.args.get('attribute')
    print("Req", school, attribute)
    
    if school == None:
        school = 'Florida Christian School MS'
    if attribute == None:
        attribute = "height"
    #print(school, attribute)
    try:    
        fig = school_by_week(attribute, school)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        title = attribute + " by week: " + school
        description = "Experimental chart"
        data = {"title":title, "description":description, "schools":SCHOOLS, "attributes":ATTRIBUTES}
        return render_template('gbe_charts/school_bar.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with School Attribute", "err":e}
        return render_template('gbe_charts/error.html', data=data)
   
@gbe_charts_blueprint.route('/gbe/growth_rate')
def growth_rate():
    # Attribute for all schools by GBE_Id
    attribute = request.args.get('attribute')
    if attribute == None:
        attribute = 'height'
    title = "Weekly values for: " + attribute
    try:
        fig = growth_rate_chart(title, attribute)
        print("Got fig")        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        description = "Plot of weekly values for selected attribute.  All schools for 2020"
        data = {"title":title, "description":description}
        return render_template('gbe_charts/growth_rate.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with School Attribute", "err":e}
        return render_template('gbe_charts/error.html', data=data)

@gbe_charts_blueprint.route('/gbe/germination')
def germination():
    # box chart of attribute

    print("Germination Rate")        
    title = "Germination Rate"
    description = "Time from planting till the first leaves appear"
    
    try:
        fig = germination_rate_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        data = {"title":title, "description":description}
        return render_template('gbe_charts/basic_chart.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with Germination Rate", "err":e}
        return render_template('gbe_charts/error.html', data=data)    

@gbe_charts_blueprint.route('/gbe/score_card')
def score_card():
    print("Score Card all Schools")
    title = "Counts of missing and invalid data from spreadsheet"
    description = "Count of missing and invalid data by school.  Data may be missing due the the plant dying and further data entry is meaningless.  Invalid data is often poor data formatting."
    try:
        fig = score_card_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        data = {"title":title, "description":description}
        return render_template('gbe_charts/basic_chart.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with Score Card", "err":e}
        return render_template('gbe_charts/error.html', data=data)

@gbe_charts_blueprint.route('/gbe/health')
def health():
    print("Health of Plots")
    title = "Health of Plots by Schools"
    description = "Average health of the plant.  The scale is converted to a number: 'good'=10, 'fair'=7, 'poor'=4, 'dead' = 1"
    try:
        print("Get data")
        fig = health_chart()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        data = {"title":title, "description":description}
        print("Render")
        return render_template('/gbe_charts/basic_chart.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with Health Chart", "err":e}
        return render_template('/gbe_charts/error.html', data=data)    
    
@gbe_charts_blueprint.route('/gbe/deaths_week')
def deaths_week():
    print("Deaths per Week")
    data = deaths_by_week()
    return render_template('/gbe_charts/deaths_week.html', data=data)

#------------------ Variety of Chart Styles for Group ---------------

@gbe_charts_blueprint.route('/gbe/histogram')
def histogram():
    # histogram of environmental variable
    attribute = request.args.get('attribute')
    if attribute == None:
        attribute = 'temp'
    title = "Histogram of: " + attribute
    try:
        fig = histogram_chart(attribute, title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        description = "Plot of weekly values for selected attribute.  All schools for 2020"
        data = {"title":title, "description":description}
        return render_template('gbe_charts/histogram.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with School Attribute", "err":e}
        return render_template('/gbe_charts/error.html', data=data)
    
    
@gbe_charts_blueprint.route('/gbe/scatter')
def scatter():
    # two variable plot
    print("Two Variable Scatter Chart")
    attribute1 = request.args.get('attribute1')
    if attribute1 == None:
        attribute1 = 'height'
    attribute2= request.args.get('attribute2')
    if attribute2 == None:
        attribute2 = 'edible_mass'        
    title = "Scatter Plot of: " + attribute1 + " vs " + attribute2
    try:
        fig = two_var_scatter_chart(attribute1, attribute2, title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        description = "Scatter plot of relationship between two variables"
        data = {"title":title, "description":description}
        return render_template('/gbe_charts/scatter.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with scatter chart", "err":e}
        return render_template('/gbe_charts/error.html', data=data)

@gbe_charts_blueprint.route('/gbe/env_scatter')
def env_scatter():
    # two variable plot
    attribute = request.args.get('attrib')
    if attribute == None:
        attribute = 'edible_mass'
    env_var = request.args.get('env_var')
    if env_var == None:
        env_var = 'temp'        
    title = "Scatter Plot of: " + attribute + " vs " + env_var
    try:
        fig = environmental_chart(env_var, attribute, title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        description = "Scatter plot of relationship between variable and environment"
        data = {"title":title, "description":description}
        return render_template('/gbe_charts/environ.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with Environmental Chart", "err":e}
        return render_template('/gbe_charts/error.html', data=data)

@gbe_charts_blueprint.route('/gbe/env_bubble')
def env_bubble():
    # two variable plot
    attribute = request.args.get('attrib')
    week = request.args.get('week')   
    if attribute == None:
        attribute = 'edible_mass'
        
    if week == None:
        week = 4
    else:
        week = int(week)
    if attribute in [EDIBLE_MASS, INEDIBLE_MASS]:
        # only collected in week 4
        week = 4
    title = "Bubble Chart of: temp & humidity vs " + attribute
    try:
        fig = full_env_chart(attribute, week, title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        description = "Scatter bubble plot of attribute and environment"
        data = {"title":title, "description":description}
        return render_template('gbe_charts/env_bubble.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with Environmental Bubble Chart", "err":e}
        return render_template('gbe_charts/error.html', data=data)

@gbe_charts_blueprint.route('/gbe/box')
def box():
    # box chart of attribute

    attribute = request.args.get('attribute')
    if attribute == None:
        attribute = 'height'
    week= request.args.get('week')
    if week == None:
        week = 4
    if attribute == EDIBLE_MASS:
        week = 4
    print("Box Chart", attribute, week)        
    title = "Box Chart of: " + attribute + " for Week " + str(week)
    try:
        fig = box_test_chart(attribute, week)
        print("Got fig")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        description = "Box Chart of Attribute"
        data = {"title":title, "description":description}
        print("Render Template")
        return render_template('gbe_charts/box.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with School Attribute", "err":e}
        return render_template('gbe_charts/error.html', data=data)

   
@gbe_charts_blueprint.route('/gbe//env', methods=['GET', 'POST'])
def env():
    # weekly change of attribute for a school
    school = request.args.get('school')
    trial = request.args.get('trial')
    attribute = request.args.get('attribute')    
    print("Req", school, trial, attribute)
    
    if school == None:
        school = 'OpenAgBloom'
    if trial == None:
        trial = "ALL"
    if attribute == None:
        attribute = CO2
    #print(school, attribute)
    if trial == "ALL":
        start_date = 0
        start_date_str = "Beginning"
        end_date = datetime.now().timestamp()*1000
        end_date_str = "Now"
    else:    
        trial_doc = get_trial(school, trial)
        start_date = trial_doc[TIME][START_DATE]
        start_date_str = trial_doc[TIME][START_DATE_STR]
        end_date = trial_doc[TIME][END_DATE]
        end_date_str = trial_doc[TIME][END_DATE_STR]
        start_date = time_test(start_date)
        end_date = time_test(end_date)
    title = "Chart of {} for {} Trial".format(attribute, trial) 
    description = "{} sensor data".format(attribute)
    page_data = {"title":title, "description":description,
            "farm":school, "trial":trial, "start_date":start_date_str, "end_date":end_date_str}        
    try:
        fig = environmental_chart("Air", attribute, title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('gbe_charts/env_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        data = {"msg":"Failure with Environmental Chart", "err":e}
        return render_template('gbe_charts/error.html', data=data)

