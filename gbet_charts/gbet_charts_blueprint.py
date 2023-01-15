from flask import Blueprint, render_template, request, abort
from jinja2 import TemplateNotFound
from datetime import datetime
import json
import plotly

gbet_charts_blueprint = Blueprint('gbet_charts_blueprint', __name__, template_folder='templates')

# Page functions
# gbet_charts
#from gbet_charts.functions.Ploty_Chart import test_chart_json, env_chart_json, dew_point_chart
from gbet_charts.functions.Group_Chart import trial_env_chart, dew_point_chart, trial_by_week_chart
from gbet_charts.functions.GBE_Data import get_trial
from functions.GBE_Util import *

# This is working
@gbet_charts_blueprint.route('/gbet')
def index():
    try:
        print('gbet/index.html')
        return render_template('gbet_charts/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@gbet_charts_blueprint.route('/gbet/', defaults={'page': 'index'})
@gbet_charts_blueprint.route('/gbet/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('gbet_charts/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
@gbet_charts_blueprint.route('/gbet/test_chart', methods=['GET', 'POST'])
def test_chart():
    try:
        graphJSON = test_chart_json()
        print(graphJSON)
        page_data = {}
        print("Render_Template")
        return render_template('gbet_charts/test_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        print("Except test_chart", e)
        abort(404)
 
@gbet_charts_blueprint.route('/gbet/dashboard', methods=['GET', 'POST'])
def dashboard():
    farm = "OpenAgBloom"
    field = "GBE_D_3"    
    from gbet_charts.functions.ImageRetrieve import get_jpg
    start_date, image_name, image = get_jpg(farm, field)
    
    try:
#         data = get_test_data('temperature')
#         page_data = get_page_data()
        page_data = {"farm":farm, "field":field, "experiment":"Exp_123_2022", "trial":"T_1", "temp":26.4, "humidity":60, "co2":1954, "light":"On", "image":image, "image_name":image_name , "image_start_date":start_date} 
#         print(page_data)
#         #fig = env_gbet_chart(attribute, school, start_date, end_date)
#         graphJSON = get_JSONgbet_chart(data, fmt)
#         print("Render_Template")
        return render_template('gbet_charts/dashboard.html', data=page_data)
    except Exception as e:
        print("Except dashboard", e)
        abort(404)
        
#--------------- GBE gbet_charts below here --------------------------
        
@gbet_charts_blueprint.route('/gbet/env', methods=['GET', 'POST'])
def env():
    trial = request.args.get('trial')
    attribute = request.args.get('attribute')
    print("Req", trial, attribute)
    
    if trial == None:
        trial = ''
    if attribute == None:
        attribute = TEMPERATURE    
    try:
        # FIX: need to get dates from trial, and attribute from input
        start_date = (datetime.now().timestamp()-(30*24*60*60))*1000
        end_date = datetime.now().timestamp()*1000
        start_date_str = '12/11/2022'
        end_date_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        trial = ''
        fig = trial_env_chart(trial, attribute, start_date, end_date)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print(graphJSON)
        page_data = {'farm':'OpenAgBloom', 'trial':123, 'start_date':start_date_str, 'end_date':end_date_str}
        print("Render_Template")
        return render_template('gbet_charts/env_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        print("Except gbet/error", e)
        abort(404)
        
@gbet_charts_blueprint.route('/gbet/dew_point', methods=['GET', 'POST'])
def dew_point():
    # weekly change of attribute for a school
    school = request.args.get('school')
    trial = request.args.get('trial')
    print("Req", school, trial)
    start_date_str = ''
    end_date_str = ''
    if school == None:
        school = 'OpenAgBloom'
    if trial == None:
        trial = "ALL"
    #print(school, attribute)
    if trial == "ALL":
        start_date = (datetime.now().timestamp()-(30*24*60*60))*1000
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
    try:
        fig = dew_point_chart(school, start_date, end_date)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        page_data = {'farm':'OpenAgBloom', 'trial':123, 'start_date':start_date_str, 'end_date':end_date_str}
        print("Render_Template")
        
        return render_template('gbet_charts/dew_point_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        #data = {"msg":"Failure with DewPoint Chart", "err":e}
        #return render_template('gbet_charts/gbe_t_error.html', data=data)        
        print("Except gbet/dew_point", e)
        abort(404)
        
        
       
@gbet_charts_blueprint.route('/gbet/plant_attr', methods=['GET', 'POST'])
def plant_attr():
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
        fig = trial_by_week_chart(attribute, school)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        title = attribute + " by week: " + school
        description = "Experimental chart"
        data = {"title":title, "description":description, "schools":SCHOOLS, "attributes":ATTRIBUTES}
        return render_template('gbet_charts/trial_bar.html', graphJSON=graphJSON, data=data)
    except Exception as e:
        data = {"msg":"Failure with School Attribute", "err":e}
        return render_template('gbet_charts/error.html', data=data)
        
      
@gbet_charts_blueprint.route('/gbet/plant_image', methods=['GET'])
def plant_image():
    # display latest jpg image or gif image
    farm = "OpenAgBloom"
    field = "GBE_D_3"    
    from gbet_charts.functions.ImageRetrieve import get_jpg
    
    start_date_str, name, image = get_jpg(farm, field)

    title = "Latest hourly jpg image"
    alt = "latest hourly plant image"

    #print(image)
    end_date_str = start_date_str
    description = "Development of plant image display"
    image_type = 'jpg'
    
    page_data = {"title":title, "description":description,
            "farm":farm,
            "field":field,
            "start_date_str":start_date_str,
            "end_date_str":end_date_str,
            "image_type":image_type,
            "alt":alt,
            "image":image
                 }        

    #print(page_data)
    try:
        print("Render Plant_Image")
        return render_template('gbet_charts/image.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting Image", "err":e}
        return render_template('error.html', data=data)
   
@gbet_charts_blueprint.route('/gbet/plant_gif', methods=['GET'])
def plant_gif():
    # display latest jpg image or gif image
    farm = "OpenAgBloom"
    field = "GBE_D_3"    
    from gbet_charts.functions.ImageRetrieve import get_gif
    start_date_str, end_date_str, name, image = get_gif(farm, field)
    title = "Daily GIF of trial"
    alt = "Daily GIF of trial"
    farm = "OpenAgBloom"
    field = "GBE_D_3"
    description = "GIF since start of trial"
    image_type = 'gif'
    
    page_data = {"title":title, "description":description,
            "farm":farm,
            "field":field,
            "start_date_str":start_date_str,
            "end_date_str":end_date_str,
            "image_type":image_type,
            "alt":alt,
            "image":image
                 }        

    #print(page_data)
    try:
        print("Render Plant_GIF")
        return render_template('gbet_charts/plant_gif.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting gif", "err":e}
        return render_template('gbet_charts/error.html', data=data)
       

